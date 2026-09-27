# Ansible Collection - derekwaters.ansible_schema

This collection provides tools for defining and testing a schema of Ansible vars.

This might be used instead of creating a bunch of custom ansible.builtin.assert calls at the beginning of every role you create.

# Basic Usage

Using this collection is as simple as a play including derekwaters.ansible_schema.assert and providing a schema filename, or an in-memory schem definition, as vars.

```yaml
---
- name: Test my variable data
  hosts: all
  connection: local
  gather_facts: false

  vars:
    test_reqd_val: is_here
    test_enum: violet
    test_integer: 20
    test_float: 2.3
    test_list:
      - collingwood
      - essendon
    test_dict:
      collingwood: true
      essendon: false

  tasks:
    - name: Check the assertion role
      ansible.builtin.include_role:
        name: assert
      vars:
        assert_schema_filename: test_schema.yml
```

The schema definition file (assert_schema_filename) should be a yaml file using the definition format outlined below. It is expected that this will be located on the control host, not on the managed host.

Alternatively, if you load or define the schema in a different fashion, you can provide an in-memory var as your schema definition with the 'assert_schema' var.

# Schema Format

Refer to [ANSIBLE_SCHEMA.md](./ANSIBLE_SCHEMA.md) for the format of the schema definitions.

# Roles

This collection includes the following role(s):

1. [assert](./roles/assert/) - This role can assert that the Ansible variable namespace contains a number of definitions matching a provided schema.

# Modules

1. [assert_var](./plugins/action/assert_var.py) - This action module applies a set of defined schema rules against a single Ansible variable, failing the assert if any of the rules are not met.

# Author

Derek Waters (derek@frisbeeworld.com) [github](https://github.com/derekwaters)