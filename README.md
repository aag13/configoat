<h1 align="center"> confiGOAT </h1>

confiGOAT is a powerful, flexible, and developer-friendly management tool for all your 
environment variables and configurations. 🔥

## Features
Here are some of the features that confiGOAT provides:

- Manage all environment variables or configuration parameters from a single setup.
- Support all development, testing, and production environments.
- Define configurations once, use it everywhere.
- Define configuration parameters using both YAML and Python scripts.
- Cast values before using them.
- Powerful reference mechanism to reuse variables *from any levels at any levels*.
- Multiple resource types in the YAML to support the vast majority of use cases.
- Support both simple use cases and complex, multi-layered nested configurations.
- Use dynamic modules to access the parameters through import interface in Python.
- Use a single exposed API to interact with the layered configurations.
- Support nested structures to model the configurations as per business needs.s

🎉🚀🌟

## Installation

confiGOAT can be installed with [pip](https://pip.pypa.io):

```bash
pip install configoat
```

Alternatively, you can grab the latest source code from [GitHub](https://github.com/aag13/configoat):

```bash
git clone https://github.com/aag13/configoat
cd configoat
pip install .
```

## How to Use

confiGOAT provides a user-friendly CLI command to initialize the configuration setup
for any project. 

1. Go to the root directory of the project and run the following command 
in the terminal. Follow the on-screen instructions to create the boilerplate that you 
can later work on. 

2. While selecting the type of configurations, choose the one that
best suits your specific project needs.
   - **Single (Only one YAML file)** : Use this for small projects where all configurations will fit in one single YAML file.
   - **Nested (Parent-child YAML files)** : Use this for projects where nested configurations and re-usage of parameters are needed.
   - **Nested with Scripts (Includes .py scripts)** : Use this for large-scale projects where multi-layered configurations need to be resolved using scripts.

    ```bash
    configoat init
    ```

3. Open the YAML file(s) and update as per your project's needs. See the examples provided
in the example files on how to add new parameters.

4. Access environment variables using get() inside any python module or script. Here, 
we are initializing the **conf** with parameters for **dev** environment. We are also
providing the namespace **all_config**, under which all the dynamic modules will be created.

    ```python3
    from configoat import conf
    conf.initialize(config="configs/main.yaml", env="dev", module="all_config")
    print(conf.get('@.var1', default='test', cast=str))
    print(conf.get('@.var7.varAA'))
    print(conf.get('@.var9.d'))
    ```

5. You can also access environment variables using dynamic modules inside any python module or script.
    ```python3
    import all_config
    print(all_config.var1)
    print(all_config.var7.varAA)
    print(all_config.var9.d)
    ```

## Issues

Please let us know if you find any issue by [filing an issue.](https://github.com/aag13/configoat/issues)

## Maintainers

- [@banna](https://github.com/Hasan-Ul-Banna) (Hasan-UL-Banna)
- [@galib](https://github.com/aag13) (Asadullah Al Galib)

👋



