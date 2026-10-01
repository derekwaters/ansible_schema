from __future__ import annotations

import re

from ansible.plugins.action import ActionBase

try:
    from ansible.module_utils.datatag import native_type_name
    native_type_name_found = True
except ImportError:
    native_type_name_found = False

def safe_native_type_name(value: object) -> str:
    if native_type_name_found:
        return native_type_name(value)
    check_types_map = {
        "str": str,
        "int": int,
        "bool": bool,
        "float": float,
        "list": list,
        "dict": dict
    }
    for check_type_label, check_type in check_types_map.items():
        if isinstance(value, check_type):
            return check_type_label
    return ""

class ActionModule(ActionBase):
    """Assert that a variable matches an expected definition."""

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = {}

        result = super().run(tmp, task_vars)
        result.update(dict(changed=False))

        validation_result, new_module_args = self.validate_argument_spec(
            argument_spec=dict(
                var_name=dict(type=str, aliases=['var_name'], required=True),
                schema=dict(type=dict, required=True),
            ),
        )

        var_name = new_module_args['var_name']
        schema = new_module_args['schema']

        # print("------------------")
        # print(var_name)
        # print("------------------")
        # print(schema)
        # print(type(schema))
        # print("------------------")

        # var_name may itself be templated
        var_name = self._templar.template(var_name)

        my_test_value = task_vars.get(var_name)

        self.failures = []

        self.check_var_against_schema(var_name, my_test_value, schema)

        if len(self.failures) > 0:
            result['failed'] = True
            result['msg'] = "\n".join(self.failures)
        else:
            result['changed'] = False
            result['msg'] = "var {0} matches schema".format(var_name)
        return result


    def check_var_against_schema(self, var_name, value, schema):
        # Check required
        if 'required' in schema and schema['required'] and value is None:
            self.failures.append("Required var {0} not defined".format(var_name))
            return

        # Check type
        if safe_native_type_name(value) != schema['type']:
            self.failures.append("var {0} of type {1} does not match expected type {2}".format(var_name, safe_native_type_name(value), schema['type']))
            return

        if self.is_numeric(value):
            # Check min_value
            if 'min_value' in schema and value < schema['min_value']:
                self.failures.append("var {0} must be greater than or equal to {1} - got {2}".format(var_name, schema['min_value'], value))

            # Check max_value
            if 'max_value' in schema and value > schema['max_value']:
                self.failures.append("var {0} must be less than or equal to {1} - got {2}".format(var_name, schema['max_value'], value))

        # Check allowed_values
        if safe_native_type_name(value) == 'str':
            if 'allowed_values' in schema and schema['type'] == 'str':
                if value not in schema['allowed_values']:
                    self.failures.append("var {0} must be one of the allowed values {1} - got {2}".format(var_name, ','.join(schema['allowed_values']), value))

            # Check min_length
            if 'min_length' in schema and len(value) < schema['min_length']:
                self.failures.append("var {0} must be {1} chars or longer - got {2}".format(var_name, schema['min_length'], len(value)))

            # Check max_length
            if 'max_length' in schema and len(value) > schema['max_length']:
                self.failures.append("var {0} must be {1} chars or shorter - got {2}".format(var_name, schema['max_length'], len(value)))

            # Check regex
            if 'regex' in schema and re.search(schema['regex'], value) is None:
                self.failures.append("var {0} must match the regular expression {1}".format(var_name, schema['regex']))

        # Check lists
        if safe_native_type_name(value) == 'list':
            # Check min_length
            if 'min_length' in schema and len(value) < schema['min_length']:
                self.failures.append("var {0} must be {1} items or longer - got {2}".format(var_name, schema['min_length'], len(value)))

            # Check max_length
            if 'max_length' in schema and len(value) > schema['max_length']:
                self.failures.append("var {0} must be {1} items or shorter - got {2}".format(var_name, schema['max_length'], len(value)))

            # Now check each item
            if 'list_values' in schema:
                for idx, list_item in enumerate(value):
                    list_item_name = "{0}[{1}]".format(var_name, idx)
                    # print("Checking {0}".format(list_item_name))
                    # print(list_item)
                    # print(schema['list_values'])
                    self.check_var_against_schema(list_item_name, list_item, schema['list_values'])

        # Check dicts
        if safe_native_type_name(value) == 'dict':

            # Now check each item
            if 'dict_values' in schema:
                for schema_def in schema['dict_values']:
                    key_name = schema_def['name']
                    dict_item_name = "{0}.{1}".format(var_name, key_name)

                    # If it's required, check that it exists
                    if 'required' in schema_def and schema_def['required']:
                        if key_name not in value:
                            self.failures.append("var {0} is required".format(dict_item_name))
                            continue

                    # If it exists, assert that it meets the schema
                    if key_name in value:
                        self.check_var_against_schema(dict_item_name, value[key_name], schema_def)

    def is_numeric(self, test_val):
        return safe_native_type_name(test_val) == 'int' or safe_native_type_name(test_val) == 'float'
