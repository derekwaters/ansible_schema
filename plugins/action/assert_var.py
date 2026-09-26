from __future__ import annotations

import typing as t

from ansible.errors import AnsibleError
from ansible.plugins.action import ActionBase
from ansible.module_utils.datatag import native_type_name

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

        print("------------------")
        print(var_name)
        print("------------------")
        print(schema)
        print(type(schema))
        print("------------------")

        # var_name may itself be templated
        var_name = self._templar.template(var_name)

        my_test_value = task_vars.get(var_name)

        # Check required
        if 'required' in schema and schema['required'] and my_test_value is None:
            result['failed'] = True
            result['msg'] = "Required var {0} not defined".format(var_name)
            return result

        # Check type
        if native_type_name(my_test_value) != schema['type']:
            result['failed'] = True
            result['msg'] = "var {0} of type {1} does not match expected type {2}".format(var_name, native_type_name(my_test_value), schema['type'])
            return result

        # Check allowed_values
        if 'allowed_values' in schema and schema['type'] == 'str':
            if my_test_value not in schema['allowed_values']:
                result['failed'] = True
                result['msg'] = "var {0} must be one of the allowed values {1} - got {2}".format(var_name, ','.join(schema['allowed_values']), my_test_value)
                return result

        # Check min_value
        if 'min_value' in schema and my_test_value < schema['min_value']:
            result['failed'] = True
            result['msg'] = "var {0} must be greater than or equal to {1} - got {2}".format(var_name, schema['min_value'], my_test_value)
            return result

        # Check max_value
        if 'max_value' in schema and my_test_value > schema['max_value']:
            result['failed'] = True
            result['msg'] = "var {0} must be less than or equal to {1} - got {2}".format(var_name, schema['max_value'], my_test_value)
            return result

        result['changed'] = False
        result['msg'] = "var {0} matches schema".format(var_name)
        return result
