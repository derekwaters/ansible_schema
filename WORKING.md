required?

var exists
var exists and has a value
var exists and has length range?
var exists and in particular set of values
      - controller_pg_sslmode in ['disable', 'allow', 'prefer', 'require', 'verify-ca', 'verify-full']
var exists and matches regex
var exists, is integer and in range
var exists, is float and in range
      - controller_percent_memory_capacity is float
      - controller_percent_memory_capacity | float <= 1.0
      - controller_percent_memory_capacity | float >= 0.01
var is a dict
var is a list with certain number of items


var has child attr?
          - _metrics_utility_settings | selectattr('setting', 'equalto', 'METRICS_UTILITY_PRICE_PER_NODE') | list | length > 0


		  for checking child keys:
		  _eda_types | difference(_eda_allowed_types) | length == 0



schema:
  - name: XXXX
    type: str, float, bool, int, list, dict
	required: true/false
	allowed_values:
	  - for_enums
	min_length:
	max_length:
	mix_value:
	max_value:
	list_values:
	dict_values: