from typing import Optional
import os
import configparser
import numpy as np
import netCDF4

FILE_PATH = os.path.dirname(os.path.realpath(__file__))


class Quality:
    """Class containing quality control routines."""

    def __init__(self, filename: str):
        self.n_metadata_tests = 0
        self.n_metadata_test_failures = 0
        self.n_data_tests = 0
        self.n_data_test_failures = 0
        self._nc = netCDF4.Dataset(filename)
        self._metadata_config = _read_config(f'{FILE_PATH}/metadata_config.ini')
        self._data_config = _read_config(f'{FILE_PATH}/data_quality_config.ini')

    def check_metadata(self) -> dict:
        """Check metadata of Cloudnet file.

        Returns:
            dict: Dictionary containing test results and some diagnostics.

        Examples:
            >>> from cloudnetpy_qc import Quality
            >>> quality = Quality('/foo/bar/categorize.nc')
            >>> result = quality.check_metadata()

        """
        return {
            'missingVariables': self._find_missing_keys('required_variables'),
            'missingGlobalAttributes': self._find_missing_keys('required_global_attributes'),
            'invalidGlobalAttributeValues': self._find_invalid_global_attribute_values(),
            'invalidDataTypes': self._find_invalid_data_types(),
            'invalidUnits': self._check_attribute('units'),
            'invalidLongNames': self._check_attribute('long_name', ignore_model=True),
            'invalidStandardNames': self._check_attribute('standard_name', ignore_model=True),
        }

    def check_data(self) -> dict:
        """Check data values of Cloudnet file.

        Returns:
            dict: Dictionary containing test results and some diagnostics.

        Examples:
            >>> from cloudnetpy_qc import Quality
            >>> quality = Quality('/foo/bar/categorize.nc')
            >>> result = quality.check_data()

        """
        return {
            'outOfBounds': self._find_invalid_data_values(),
            'timeVectorStep': self._check_time_vector()
        }

    def close(self) -> None:
        """Close the inspected file."""
        self._nc.close()

    def _check_median_lwp(self):
        invalid = []
        if self._nc.cloudnet_file_type != 'mwr' or 'lwp' not in self._nc.variables:
            return invalid
        min_threshold = 0
        max_threshold = 10
        median_lwp = np.median(self._nc.variables['lwp'][:]) / 1000
        if not (min_threshold < median_lwp < max_threshold):
            invalid.append(('median lwp',
                            (median_lwp, median_lwp),
                            f'{str(min_threshold), str(max_threshold)}'))

    def _check_time_vector(self):
        invalid = []
        time = self._nc['time'][:]
        if len(time) == 1:
            return invalid
        differences = np.diff(time)
        min_difference = np.min(differences)
        max_difference = np.max(differences)

        if min_difference <= 0 or max_difference >= 24:
            invalid.append(('time step difference x 1e5', (round(min_difference*1e5),
                                                           round(max_difference*1e5)), '0, 24'))
            self.n_data_test_failures += 1
        return invalid

    def _find_invalid_data_values(self) -> list:
        invalid = []
        for var, limits in self._data_config.items('limits'):
            if var in self._nc.variables:
                self.n_data_tests += 1
                limits = tuple(map(float, limits.split(',')))
                max_value = np.max(self._nc.variables[var][:])
                min_value = np.min(self._nc.variables[var][:])
                if min_value < limits[0] or max_value > limits[1]:
                    invalid.append((var, (min_value, max_value), limits))
                    self.n_data_test_failures += 1
        return invalid

    def _find_invalid_global_attribute_values(self) -> list:
        invalid = []
        for key, limits in self._metadata_config.items('attribute_limits'):
            if hasattr(self._nc, key):
                self.n_metadata_tests += 1
                limits = tuple(map(float, limits.split(',')))
                value = int(self._nc.getncattr(key))
                if not limits[0] <= value <= limits[1]:
                    invalid.append((key, value, limits))
                    self.n_metadata_test_failures += 1
        return invalid

    def _check_attribute(self, name: str, ignore_model: Optional[bool] = False):
        invalid = []
        if ignore_model is True and self._nc.cloudnet_file_type == 'model':
            return invalid
        for key, expected in self._metadata_config.items(name):
            if key in self._nc.variables:
                self.n_metadata_tests += 1
                value = getattr(self._nc.variables[key], name, '')
                if value != expected:
                    invalid.append((key, value, expected))
                    self.n_metadata_test_failures += 1
        return invalid

    def _find_invalid_data_types(self) -> list:
        invalid = []
        for key in self._nc.variables:
            expected_value = 'float32'
            self.n_metadata_tests += 1
            value = self._nc.variables[key].dtype.name
            for config_key, custom_value in self._metadata_config.items('data_types'):
                if config_key == key:
                    expected_value = custom_value
                    break
            if value != expected_value:
                if key == 'time' and value in ('float32', 'float64'):
                    continue
                invalid.append((key, value, expected_value))
                self.n_metadata_test_failures += 1
        return invalid

    def _find_missing_keys(self, config_section: str) -> list:
        nc_keys = self._nc.ncattrs() if 'attr' in config_section else self._nc.variables.keys()
        config_keys = self._read_config_keys(config_section)
        missing_keys = list(set(config_keys) - set(nc_keys))
        self.n_metadata_tests += len(config_keys)
        self.n_metadata_test_failures += len(missing_keys)
        return missing_keys

    def _read_config_keys(self, config_section: str) -> np.ndarray:
        field = 'all' if 'attr' in config_section else self._nc.cloudnet_file_type
        keys = self._metadata_config[config_section][field].split(',')
        return np.char.strip(keys)


def _read_config(filename: str) -> configparser.ConfigParser:
    conf = configparser.ConfigParser()
    conf.optionxform = str
    conf.read(filename)
    return conf
