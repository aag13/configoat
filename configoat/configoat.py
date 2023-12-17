import enum
import os
import types
import sys
import yaml
import copy
import importlib.util
import re

DEFAULT_ROOT_CONFIG = "main.yaml"
DEFAULT_ROOT_MODULE = "root_config"
META_TYPE_KEY = "__type"
ENV_NAME = "CONFIGOAT_ENVIRONMENT"
# REFERENCE_PREFIX = "$ref"
# REFERENCE_HOME = "@"


class ConfiGOAT:
    def __init__(self):
        self._data_dict = None
        self._environment = None
        self._root_config = DEFAULT_ROOT_CONFIG
        self._root_module = DEFAULT_ROOT_MODULE

    def get(self, key, default=None, cast=None):
        copy_data = copy.deepcopy(self._data_dict)
        modules = key.split('.')
        if modules[0] == '@':
            modules = modules[1:]
        else:
            raise InvalidAccessKeyExeption(
                "Invalid Access Key. Access Key must start with '@' to denote root config. Key ({})".format(key))

        try:
            for m in modules:
                copy_data = copy_data[m]

            return copy_data.get('value', default) if cast is None else cast(copy_data.get('value', default))
        except KeyError:
            return default if cast is None else cast(default)

    def initialize(self, config=None, env=None, module=None):
        if not env:
            raise ValueError("Must provide an environment")

        self._root_config = config if config is not None else self._root_config
        self._root_module = module if module is not None else self._root_module
        self._environment = env
        os.environ.setdefault(ENV_NAME, self._environment)
        self._data_dict = self._build_data_dict(self._root_config, '@')
        self._update_reference_value(self._data_dict)
        self._initiate_dynamic_module()

    def _update_reference_value(self, current_dict):
        for key in {key: value for key, value in current_dict.items() if isinstance(value, dict)}:
            if current_dict[key]['__type'] in [ResourceTypeEnum.COMMON.value, ResourceTypeEnum.NORMAL.value, ResourceTypeEnum.DEFAULT.value]:
                if current_dict[key]['__ref']:
                    current_dict[key]['value'] = self._reference_resolver(current_dict[key]['__ref'])
            elif current_dict[key]['__type'] in [ResourceTypeEnum.NESTED.value, ResourceTypeEnum.SCRIPT.value]:
                self._update_reference_value(current_dict[key])

    def _build_data_dict(self, config_path, parent_path):
        current_dict = {}
        with open(config_path, 'r') as file:
            try:
                data = yaml.safe_load(file)
                data = data['resources']
                for key in data:
                    resource_type = data[key]['type']
                    value = data[key].get('value', None)
                    if resource_type == ResourceTypeEnum.COMMON.value:
                        current_dict[key] = self._get_unresolved_value(value, resource_type, parent_path)
                    elif resource_type == ResourceTypeEnum.NORMAL.value:
                        value = value[self._environment]
                        current_dict[key] = self._get_unresolved_value(value, resource_type, parent_path)
                    elif resource_type == ResourceTypeEnum.NESTED.value:
                        current_dict[key] = self._build_data_dict(data[key]['path'], '{}.{}'.format(parent_path, key))
                        current_dict[key][META_TYPE_KEY] = resource_type
                    elif resource_type == ResourceTypeEnum.SCRIPT.value:
                        should_flat = data[key].get('flat', False)
                        parsed_dict = self._script_parser(data[key]['path'], data[key]['variable_list'])
                        if should_flat:
                            current_dict.update(parsed_dict)
                        else:
                            current_dict[key] = parsed_dict
                            current_dict[key][META_TYPE_KEY] = resource_type
                    else:
                        raise YAMLFormatException("Invalid YAML KeyType. KeyType ({})".format(resource_type))
            except:
                raise YAMLFormatException("Invalid YAML format. Key ({})".format(key))
            return current_dict

    def _get_unresolved_value(self, val_or_ref, resource_type, parent_path=None):
        val_dict = {
            '__type': resource_type,
            '__ref': None,
            'value': val_or_ref,
        }
        if isinstance(val_or_ref, str) and '$ref' in val_or_ref:
            val_dict.update({
                '__ref': self._get_absolute_ref(val_or_ref, parent_path),
                'value': None
            })

        return val_dict

    def _get_absolute_ref(self, value, parent_path):
        for reference in set(self._extract_references(value)):
            if not reference.startswith('@.'):
                old = '$ref({})'.format(reference)
                new = '$ref({}.{})'.format(parent_path, reference)
                value = value.replace(old, new)
        return value

    def _extract_references(self, reference_string):
        pattern = r'\$ref\((.*?)\)'
        matches = re.findall(pattern, reference_string)
        return matches

    def _script_parser(self, script_path, variable_list):
        current_dict = {}
        spec = importlib.util.spec_from_file_location('module', script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for var in variable_list:
            value = getattr(module, var)
            current_dict[var] = self._get_unresolved_value(value, ResourceTypeEnum.DEFAULT.value)
        return current_dict

    def _get_reference_value(self, reference, references_seen):
        copy_data = copy.deepcopy(self._data_dict)
        modules = reference.split('.')
        for m in modules:
            copy_data = copy_data[m]
        if copy_data['__ref'] is not None:
            copy_data['value'] = self._reference_resolver(copy_data['__ref'], references_seen)

        return copy_data['value']

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
        pattern = r'\$ref\(@\.(.*?)\)'
        matches = re.finditer(pattern, reference_string)

        for match in matches:
            reference_key = match.group(1)
            if reference_key in references_seen:
                replacement_value = references_seen[reference_key]
                reference_string = reference_string.replace(match.group(0), str(replacement_value))

        return reference_string

    def _create_module(self, mod_dict, mod_name, parent=""):
        current_module = types.ModuleType(mod_name)
        mod_with_parent = mod_name if parent == "" else "{}.{}".format(parent, mod_name)

        for key, val in mod_dict.items():
            if not isinstance(val, dict):
                continue

            if isinstance(val, dict) and val.get(META_TYPE_KEY) in [ResourceTypeEnum.NESTED.value, ResourceTypeEnum.SCRIPT.value]:
                # this is a dict for nested/script module, handle recursively
                val_or_mod = self._create_module(val, key, mod_with_parent)
            else:
                val_or_mod = val.get('value')

            setattr(current_module, key, val_or_mod)

        sys.modules[mod_with_parent] = current_module
        return current_module

    def _initiate_dynamic_module(self):
        root_module = self._create_module(self._data_dict, self._root_module)

    def _validate_reference(self):
        print(self._data_dict)

    def __call__(self, key, default=None, cast=None):
        return self.get(key=key, default=default, cast=cast)


conf = ConfiGOAT()


class YAMLFormatException(Exception):
    pass

class CircularImportExeption(Exception):
    pass

class InvalidAccessKeyExeption(Exception):
    pass

class ModuleAccessException(Exception):
    pass

class ResourceTypeEnum(enum.Enum):
    COMMON = "common"
    NORMAL = "normal"
    NESTED = "nested"
    SCRIPT = "script"
    DEFAULT = "default"
