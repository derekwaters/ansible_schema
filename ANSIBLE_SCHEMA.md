# Ansible Schema

## Introduction

The Ansible Schema format defines a list

The top level of the schema must be a dict with a single key named 'schema', whose value is a list of schema definition objects.

## Schema Definition Objects

Each schema object defines schema validation for a single Ansible var. The schema object can have the following fields:

| Field Name | Required? | Type | Applies To | Description |
|------------|-----------|------|------------|-------------|
| name | yes | str | Any | This field must be the name of the variable to assert |
| type | yes | str | Any | This field defines the Python type of the variable. Valid values are [str, float, bool, int, list, dict] |
| required | no | bool | Any | This field is used to define whether a variable or a child object must be defined for the schema to be valid |
| allowed_values | no | list of str | str | This field lists valid string values for a str field (ie. an enum type) |
| min_length | no | int | str, list | This field defines the minimum length (inclusive) of a string or list |
| max_length | no | int | str, list | This field defines the maximum length (inclusive) of a string or list |
| min_value | no | int, float | int, float | This field defines the minimum value (inclusive) of an int or float |
| max_value | no | int, float | int, float | This field defines the maximum value (inclusive) of an int or float |
| list_values | no | dict | list | This field defines a child schema which will be applied to all of this variable's child list items |
| dict_values | no | list of dict | dict | This field defines a list of schema objects where the name matches the key of the variable's dict, and the schema definition must match the object referenced by that key |

## Example Schema

A sample schema is shown below.

```yaml
---
schema:
  - name: test_reqd_val
    required: true
    type: str
  - name: test_enum
    type: str
    allowed_values:
      - red
      - orange
      - yellow
      - green
      - blue
      - indigo
      - violet
  - name: test_integer
    type: int
    min_value: 1
    max_value: 20
  - name: test_float
    type: float
    min_value: 2.0
  - name: test_list
    type: list
    list_values:
      type: str
      allowed_values:
        - adelaide
        - brisbane
        - carlton
        - collingwood
        - essendon
        - geelong
```
