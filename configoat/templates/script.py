import math
import os

a = 100

if os.environ.get("CONFIGOAT_ENVIRONMENT", "dev") == "dev":
    b = "hello from dev"
else:
    b = 'hello from non-dev'

c = math.sqrt(5)

# $ref(@.var7.varCC) -> references the variable 'varCC' which is inside the variable 'var7' which is inside the main YAML file
d = "$ref(@.var7.varCC)_test"

# $ref(@.var2) -> references the variable 'var2' which is inside the main YAML file
e = "$ref(@.var2)_test"
