assert
=========

This role prepares a defined Ansible variable schema, and then asserts that the current Ansible variable namespace matches the schema.

Requirements
------------

None.

Role Variables
--------------

This role requires one of the two following variables:

1. assert_schema_filename - The path to a schema definition file in YAML format. Refer to the schema definition documentation for the contents of this file. The file should be located on the Ansible control host, not on the managed host.
2. assert_schema - If the schema is being provided in-memory, this var should be passed as a dict, with a single schema key containing a list of schema objects. Refer to the schema definition documentation for the structure of this data.

Dependencies
------------

None.

Example Playbook
----------------

Example usage of this role is shown below.

```yaml
---
- name: Ensure all of our required variables are set properly.
  hosts: all
  tasks:
    - name: Assert that our variables meet the schema
      ansible.builtin.include_role:
        name: derekwaters.ansible_schema.assert
      vars:
        assert_schema_filename: test_schema.yml
```

License
-------

BSD

Author Information
------------------

Derek Waters (derek@frisbeeworld.com) - https://github.com/derekwaters/