#Validate brackets
This package allows to validate correct opening and closing of brackets in a string.

## Installation
Run the following to install:
```
$pip install validate_brackets
```


# Usage
```
from ValidateBrackets import validate_brackets

# Validate a string with brackets, returns True
validate_brackets('[]{()}')

# Validate a string with brackets, returns False
validate_brackets('[]{(}'
```
# Developing validate_brackets
To install validate_brackets, along with the tool you need to develp and run tests, run the following in your virtualenv

```
$pip install -e .[dev]
```
