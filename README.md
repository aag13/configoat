<h1 align="center"> confiGOAT </h1>

confiGOAT is a powerful, flexible, and developer-friendly configuration management tool. 🔥

Features:

- Manage all your environment variables or configuration parameters from a single setup.
- Support all your development, testing, and production environments.
- Define configuration parameters using both YAML and Python scripts.
- Cast values before using them.
- Support both simple and straightforward use cases as well as complex and multi-layered 
nested structures.
- Use dynamic modules to access the parameters through imports.
- Use a single exposed API to interact with the layered configurations.
- Support nested structures to model the configurations as per business needs.
- Powerful reference mechanism to reuse variables *from any levels at any levels* 
regardless of where in the hierarchy it is defined.
- 4 different resource types in the YAML to support the vast majority of use cases.

## Installation

confiGOAT can be installed with [pip](https://pip.pypa.io):

```bash
$ pip install configoat
```

Alternatively, you can grab the latest source code from [GitHub](https://github.com/aag13/configoat):

```bash
$ git clone https://github.com/aag13/configoat
$ cd configoat
$ pip install .
```

## How to Use confiGOAT

confiGOAT is very powerful and easy to use. Since you need to define your all the 
environment variables


You can initialize the package using the following management command.
```bash
$ configoat init
```



Access environment variables using get() inside any python module/script
```python3
>>> from configoat import conf
>>> conf.initialize(config="configs/main.yaml", env="dev", module="all_config")
>>> print(conf.get('@.var1', default='test', cast=str))
>>> print(conf.get('@.var1'))
>>> print(conf.get('@.var3'))
>>> print(conf.get('@.var5'))
>>> print(conf.get('@.var7.varAA'))
>>> print(conf.get('@.var7.varBB'))
>>> print(conf.get('@.var7.varCC'))
>>> print(conf.get('@.var8'))
>>> print(conf.get('@.var9.d'))
>>> print(conf.get('@.var9.e'))
```

Access environment variables using dynamic modules inside any python module/script
```python3
>>> import all_config
>>> print(all_config.var1)
>>> print(all_config.var3)
>>> print(all_config.var5)
>>> print(all_config.var7.varAA)
>>> print(all_config.var7.varBB)
>>> print(all_config.var7.varCC)
>>> print(all_config.var8)
>>> print(all_config.var9.d)
>>> print(all_config.var9.e)
```

## Documentation

confiGOAT has usage and reference documentation at [confiGOAT.readthedocs.io](https://github.com/aag13/configoat/blob/main/README.rst).


## Contributing

confiGOAT happily accepts contributions. Please see our
[contributing documentation](https://github.com/aag13/configoat/blob/main/CONTRIBUTING.rst)
for some tips on getting started.


## Maintainers

- [@banna](https://github.com/Hasan-Ul-Banna) (Hasan-UL-Banna)
- [@galib](https://github.com/aag13) (Asadullah Al Galib)

👋



