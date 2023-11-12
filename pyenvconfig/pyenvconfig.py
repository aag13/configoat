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
        for m in modules:
            copy_data = copy_data[m]

        if isinstance(copy_data, str) and "$ref" in copy_data:
            # do recursive
            pass
        else:
            return copy_data

        # copy_data does not include $ref, then return copy_data
        # else resolve $ref recursively, use memoization




    def initialize(self, config=None, env=None, module=None):
        # assert env is not None and env != ""

        if config is not None:
            self._root_config = config

        if module is not None:
            self._root_module = module

        self._root_config = self._validate_config_path(config)
        self._environment = env

        self._data_dict = self._build_data_dict(self._root_config)
        self._validate_reference()
        self._initiate_dynamic_module()

    def _validate_config_path(self, file_path):
        return file_path

    def _build_data_dict(self, config_path):
        current_dict = {}
        with open(config_path, 'r') as file:
            data = yaml.safe_load(file)
            data = data['resources']
            try:
                for key in data:
                    if data[key]['type'] == 'common':
                        current_dict[key] = data[key]['value']
                    elif data[key]['type'] == 'normal':
                        current_dict[key] = data[key]['value'][self._environment]
                    elif data[key]['type'] == 'nested':
                        current_dict[key] = self._build_data_dict(data[key]['path'])
                        current_dict[key][META_TYPE_KEY] = 'nested'
                    elif data[key]['type'] == 'script':
                        current_dict[key] = self._script_parser(data[key]['path'], data[key]['variable_list'])

            except:
                raise YAMLFormatException("Invalid YAML format. Key ({})".format(key))

            return current_dict

    def _script_parser(self, script_path, variable_list):
        current_dict = {}
        spec = importlib.util.spec_from_file_location('module', script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for var in variable_list:
            value = getattr(module, var)
            # if '$ref' in value:
            #     references = self._extract_references(value)
            #     value = self._reference_resolver(value, references)
            current_dict[var] = value
        return current_dict

    def _extract_references(self, reference_string):
        pattern = r'\$ref\((.*?)\)'
        matches = re.findall(pattern, reference_string)
        return matches

    def _reference_resolver(self, main_string, references):
        return main_string

    def _create_module(self, mod_dict, mod_name, parent=""):
        current_module = types.ModuleType(mod_name)
        mod_with_parent = mod_name if parent == "" else "{}.{}".format(parent, mod_name)

        for key, val in mod_dict.items():
            val_or_mod = val
            if type(val) == dict and val.get(META_TYPE_KEY, None):
                # this is a dict for nested module, handle recursively
                del val[META_TYPE_KEY]
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


