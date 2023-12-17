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

### Initial Setup
confiGOAT provides a user-friendly CLI command to initialize the configuration setup
for your project. 

1. Go to the root directory of your project and run the following command 
in the terminal.

    ```bash
    configoat init
    ```

2. For the directory name, enter the name of the folder that will contain all
the configuration files and scripts. E.g. *"environments/"* will create a directory
inside the root directory of your project. Default is *"configs/"*.
3. For the main configuration file, provide a name that confiGOAT will look
for when initializing the setup for your project. (we will see how to do that
later). Default is *"main.yaml"*.
4. While selecting the type of configurations, you have 3 options. Choose the one that
best suits your specific project needs. 👇
   - **Single (Only one YAML file)** : Use this for small projects where all your configurations will fit 
   in one single YAML file.
   - **Nested (Parent-child YAML files)** : Use this for projects where it makes sense to structure the 
   configuration files in a nested hierarchy.
   - **Nested with Scripts (Includes .py scripts)** : Use this for large-scale projects where some  
   configurations need to be resolved using python scripts on top of a multi-layered hierarchy.

For example, if you can fit all your configuration variables in a single file, choose option 1. Choose option 
2 if you want to structure all the configuration parameters in separate files based on their types, such as, 
security configurations in *security.yaml* file and database configurations in *database.yaml* file. Option 3 
is best suited for cases where you need both the nested hierarchy structure and need to resolve values 
for some parameters that require executing some code. 

❄️❄️❄️

### Preparing Configuration Files
Now that you have set up the configuration folder and starting file(s), you need to populate all your 
configuration and environment variables in the generated YAML and python script files.
1. First, open the *main.yaml* (or whatever name you gave during the initial setup) file.
2. Each YAML file has 2 root properties, namely *doc* and *resources*. 👇
   - You can use *doc* to provide basic description on the type of environment or configuration variables 
   which are defined in this YAML. 
   - *resources* contains all the configuration variables that are defined in this file. If you want to 
   create a new variable, you need to define it inside *resources*. 
   ```yaml
   doc: 'This is the main config file where the processing starts from'
   resources:
   ...
   ```
3. You can define 4 different types of resources in confiGOAT. 👇
   - *normal* : Use this type if the value of the variable will be different for different environments. You can
   use different data types for different environments, such as string, integer, float, boolean, list, and dictionary.
   ```yaml
   var1:
     type: 'normal'
     value:
       dev: 'value of var1 for dev'
       stage: 'value of var1 for stage'
       uat: 'value of var1 for uat'
       production: 'value of var1 for production'
       qa: 'value of var1 for qa'
   ```
   - *common* : Use this type if the value of the variable will be same across all environments. We support
   the following data types - string, integer, float, boolean, list, and dictionary.
   ```yaml
   var2:
     type: 'common'
     value: "value of var2"
   
   var3:
     type: 'common'
     value: False
   
   var4:
     type: 'common'
     value: 100
   
   var5:
     type: 'common'
     value: [ "Banana", "Mango", "Apple" ]
   
   var6:
     type: 'common'
     value: {
       "name": "Raihan Boss",
       "age": 66,
       "address": {
         "city": "Dhaka",
         "country": "Bangladesh",
       }
     }
   ```
   - *nested* : Use this type for a nested YAML file (Available if you chose option 2 and 3 during setup). *path* 
   is the relative path from the project root folder to that nested YAML file, e.g. *configs/yamls/nested.yaml*. ✨ 
   All the variables which are defined in the specified nested YAML file will be available under the 
   namespace of the *var7* variable.
   ```yaml
   var7:
     type: 'nested'
     path: 'path/from/project/root/to/nested.yaml'
   ```
   - *script* : Use this type for a python script file (Available if you chose option 3 during setup). *path* 
   is the relative path from the project root folder to that nested script file, e.g. *configs/scripts/script.py*. ✨ 
   Only the variables which are defined in the *variable_list* property will be available from specified 
   nested script file under the namespace of the *var9* variable.
   ```yaml
   var9:
     type: 'script'
     variable_list: ['a', 'b', 'c', 'd', 'e']
     path: 'path/from/project/root/to/script.py'
   ```
4. For the *nested* type, confiGOAT will process the specified YAML file **recursively**, so that if 
   the nested YAML file contains other *nested* variables, it will resolve all those nested YAML files 
   recursively as well. 👀
5. If you want to reuse the value from another variable using reference, either in the same file or any file 
in the configuration hierarchy, you need to use **$ref(variable_name)** format by replacing the 
variable_name with the actual variable in your configuration that you want to refer to. 👇
   ```yaml
   var8:
     type: 'common'
     value: "$ref(var7.varAA)"
   ```
   - Here, we are creating a new variable of type *common* by referencing the value from another variable 
   called *varAA* which is nested inside the variable *var7*.
   - If the variable is defined in any other file, then you have to provide the full *dot notation path* 
   to that variable from the main configuration file, e.g. *$ref(@.PROJECT_CODE)* refers to the variable 
   *PROJECT_CODE* defined in the root configuration YAML file. See the *nested.yaml* file for 
   an example on how to use the dot notation path for referencing a variable.

NOTE: Referencing a variable is bidirectional and depth agnostic, meaning that any variable can be referenced 
**at any depth from any depth in any direction**, as long as no circular dependency is created during 
referencing another variable. *Circular Dependency* means that definitions of two variables are dependent 
on each other and neither variable can be resolved due to this dependency. In case of circular dependency, 
confiGOAT will raise an exception indicating the circular dependency.

🌟🌟🌟

### Using Configuration Parameters in the Project

Now that you have prepared the configurations for your project, you need to use them in your project. 

1. First, you need to initialize and load all the configuration and environmental variables from the setup.
   ```python3
   from configoat import conf
   conf.initialize(config="configs/main.yaml", env="dev", module="all_config")
   ```
   - *config* denotes the path to the main configuration YAML file to start loading the variables from.
   - *env* denotes which environment the variables should be loaded for.
   - *module* denotes the name of the namespace under which all variables will be made available in the 
   dynamic module access.
2. To access the configuration variables, you have 2 options.
   - *Dot notation* : You can use the *conf* object to access any variable by providing its full 
   *dot notation path* from the root configuration file. *@* below denotes the root of the configuration, 
   the main configuration file. You can also pass the *conf* variable around like any other variable in python
   and access values like shown below.
   ```python3
   print(conf("@.VARIABLE_NAME"))
   print(conf("@.NESTED.VARIABLE_NAME"))
   
   print(conf.get("@.VARIABLE_NAME"))
   print(conf.get("@.NESTED.VARIABLE_NAME"))
   ```
   - *Dynamic module* : Use python's module and import mechanism to access any configuration 
   variable. In this approach, you import the module that you defined during the initialization step. 
   When confiGOAT initialized your configuration variables, it also created dynamic modules and attributes 
   in those modules following your configuration nested hierarchy. All these dynamic modules are inserted 
   under the provided namespace, e.g. the *all_config* module name. You can import this module anywhere in 
   your project and use the variables like any other modules and their attributes.
   ```python3
   import all_config
   print(all_config.var3)
   print(all_config.var2.var4)
   ```

**You can also provide a default value in case the variable is not found and a casting function to transform
the final value**.
```python3
print(conf("@.VARIABLE_NAME", default=10, cast=int))

print(conf.get("@.VARIABLE_NAME", default=10, cast=int))
```


## Issues

Please let us know if you find any issue by [filing an issue.](https://github.com/aag13/configoat/issues)

## Maintainers

- [@banna](https://github.com/Hasan-Ul-Banna) (Hasan-UL-Banna)
- [@galib](https://github.com/aag13) (Asadullah Al Galib)

👋



