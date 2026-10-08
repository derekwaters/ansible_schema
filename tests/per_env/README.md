# Example "Per Environment" Testing Using ansible_schema.assert

This sample test playbook allows you to validate a set of environmental values that may need to be configured and set differently across environments.

In this example, we have a var called target_env which can be 'prod' or 'nonprod' to define the environment.

We then provide {{ target_env }}_expected.yml files with definitions of certain values we expect to differ in each environment.

The test_env_schema.yml then uses a sample template which populates a bunch of var definitions (testing_vars.j2) to validate against the defined schema.

# Basic Usage

This sample test playbook operates with a single 'localhost' inventory, and can test different environments by passing target_env as an extra var on the command line.

```bash
ansible-playbook -i inventory -e target_env=nonprod test_env_schema.yml
ansible-playbook -i inventory -e target_env=prod test_env_schema.yml
```

Currently the prod test fails because the instance type is the same for nonprod and prod in testing_vars.j2.
The nonprod test fails because the storage value for nonprod is incorrect in testing_vars.j2 (should be 200, not 300)