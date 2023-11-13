import os
import types
import sys
import yaml
import copy
import importlib.util
import re

DEFAULT_ROOT_CONFIG = "config.yaml"
DEFAULT_ROOT_MODULE = "root_config"
META_TYPE_KEY = "__type"
# REFERENCE_PREFIX = "$ref"
# REFERENCE_HOME = "@"


class PyEnvConfig:
    def __init__(self):
        self._data_dict = None
        self._environment = None
        self._root_config = DEFAULT_ROOT_CONFIG
        self._root_module = DEFAULT_ROOT_MODULE

    def get(self, key):
        copy_data = copy.deepcopy(self._data_dict)
        modules = key.split('.')

        if modules[0] == '@':
            modules = modules[1:]
        else:
            raise InvalidAccessKeyExeption("Invalid Access Key. Access Key must start with '@.' to denote root config. Key ({})".format(key))
        for m in modules:
            copy_data = copy_data[m]
        if isinstance(copy_data, str) and '$ref' in copy_data:
            copy_data = self._reference_resolver(copy_data)
        elif isinstance(copy_data, dict) and META_TYPE_KEY in copy_data:
            raise ModuleAccessException("Can not access module. Key ({})".format(key))
        return copy_data

    def initialize(self, config=None, env=None, module=None):
        self._root_config = config if config is not None else self._root_config
        self._environment = env
        self._data_dict = self._build_data_dict(self._root_config, '@')
        print(self._data_dict)
        self._initiate_dynamic_module()

    def _build_data_dict(self, config_path, parent_path):
        current_dict = {}
        with open(config_path, 'r') as file:
            data = yaml.safe_load(file)
            data = data['resources']
            try:
                for key in data:
                    if data[key]['type'] == 'common':
                        value = data[key]['value']
                        if isinstance(value, str) and '$ref' in value:
                            value = self._update_path(value, parent_path)
                        current_dict[key] = value
                    elif data[key]['type'] == 'normal':
                        value = data[key]['value'][self._environment]
                        if isinstance(value, str) and '$ref' in value:
                            value = self._update_path(value, parent_path)
                        current_dict[key] = value
                    elif data[key]['type'] == 'nested':
                        current_dict[key] = self._build_data_dict(data[key]['path'], '{}.{}'.format(parent_path, key))
                        current_dict[key][META_TYPE_KEY] = 'nested'
                    elif data[key]['type'] == 'script':
                        current_dict[key] = self._script_parser(data[key]['path'], data[key]['variable_list'])
                        current_dict[key][META_TYPE_KEY] = 'script'
                    else:
                        raise YAMLFormatException("Invalid YAML KeyType. KeyType ({})".format(data[key]['type']))
            except:
                raise YAMLFormatException("Invalid YAML format. Key ({})".format(key))
            return current_dict

    def _update_path(self, value, parent_path):
        references = {}
        for reference in self._extract_references(value):  # extract only values without @.
            if not reference.startswith('@.'):
                references[reference] = '{}.{}'.format(parent_path, reference)
        if references:
            value = self._build_reference_value(value, references)
        return value

    def _script_parser(self, script_path, variable_list):
        current_dict = {}
        spec = importlib.util.spec_from_file_location('module', script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for var in variable_list:
            value = getattr(module, var)
            current_dict[var] = value
        return current_dict

    def _get_reference_value(self, reference, references_seen):
        copy_data = copy.deepcopy(self._data_dict)
        modules = reference.split('.')
        for m in modules:
            copy_data = copy_data[m]
        if isinstance(copy_data, str) and '$ref' in copy_data:
            self._reference_resolver(copy_data, references_seen)
        return copy_data
    def _extract_references(self, reference_string):
        pattern = r'\$ref\((.*?)\)'
        matches = re.findall(pattern, reference_string)
        return matches

    def _reference_resolver(self, reference_string, references_seen=None):
        references_seen = {} if references_seen is None else references_seen
        references = set(self._extract_references(reference_string))
        for reference in references:
            if reference.startswith('@.'):
                reference = reference[2::]
            else:
                raise YAMLFormatException("Invalid YAML format. Key ({})".format(reference))
            if reference not in list(references_seen.keys()):
                references_seen[reference] = 'ref'
                references_seen[reference] = self._get_reference_value(reference, references_seen)
            elif references_seen.get(reference) == 'ref':
                raise CircularImportExeption("Circular reference detected. Reference ({})".format(reference))
        return self._build_reference_value(reference_string, references_seen)


    def _build_reference_value(self, reference_string, references_seen):
        # Define the regular expression pattern
        pattern = r'\$ref\((.*?)\)'
        def replacement_callback(match):
            key = match.group(1)
            return references_seen.get(key, f'$ref({key})')  # Use the original expression if key not found

        # Use re.sub with the callback function to replace all matches
        result_string = re.sub(pattern, replacement_callback, reference_string)

        return result_string
    def _create_module(self, mod_dict, mod_name, parent=""):
        current_module = types.ModuleType(mod_name)
        mod_with_parent = mod_name if parent == "" else "{}.{}".format(parent, mod_name)

        for key, val in mod_dict.items():
            val_or_mod = val
            if isinstance(val, dict) and val.get(META_TYPE_KEY, None):
                # this is a dict for nested module, handle recursively
                val_or_mod = self._create_module(val, key, mod_with_parent)

            setattr(current_module, key, val_or_mod)

        sys.modules[mod_with_parent] = current_module
        return current_module

    def _initiate_dynamic_module(self):
        root_module = self._create_module(self._data_dict, self._root_module)

    def _validate_reference(self):
        print(self._data_dict)


    def __call__(self, key):
        return self.get(key)


myconfig = PyEnvConfig()


class YAMLFormatException(Exception):
    pass

class CircularImportExeption(Exception):
    pass

class InvalidAccessKeyExeption(Exception):
    pass

class ModuleAccessException(Exception):
    pass

