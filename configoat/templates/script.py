import math

a = 100
b = 'hello'
c = math.sqrt(5)

# $ref(@.var7.varCC) -> references the variable 'varCC' which is inside the variable 'var7' which is inside the main YAML file
d = "$ref(@.var7.varCC)_test"

# $ref(@.var2) -> references the variable 'var2' which is inside the main YAML file
e = "$ref(@.var2)_test"
