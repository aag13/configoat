<h1 align="center"> confiGOAT </h1>

confiGOAT is a powerful, flexible, and developer-friendly management tool for all your 
environment variables and configurations. 🔥🔥🔥

## Features
Here are some of the features that confiGOAT provides:

- Manage all environment variables or configuration parameters from a single setup.
- Support all development, testing, and production environments.
- Define configurations once, use it everywhere.
- Define configuration parameters using both YAML and Python scripts.
- Cast values before using them.
- Powerful reference mechanism to reuse variables *from any levels at any levels in any direction*.
- Multiple resource types in the YAML to support the vast majority of use cases.
- Support both simple use cases and complex, multi-layered nested configurations.
- Use dynamic modules to access the parameters through import interface in Python.
- Use a single exposed API to interact with the layered configurations.
- Support nested structures to model the configurations as per business needs.

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
       "name": "Raihan The Boss",
       "age": 66,
       "address": {
         "city": "Dhaka",
         "country": "Bangladesh",
       }
     }
   ```
   - *nested* : Use this type for a nested YAML file (Available if you chose option 2 or 3 during setup). *path* 
   is the relative path from the project root folder to that nested YAML file, e.g. *configs/yamls/nested.yaml*. 
   All the variables which are defined in the specified nested YAML file will be available under the 
   namespace of the *var7* variable. ✨
   ```yaml
   var7:
     type: 'nested'
     path: 'path/from/project/root/to/nested.yaml'
   ```
   - *script* : Use this type for a python script file (Available if you chose option 3 during setup). *path* 
   is the relative path from the project root folder to that nested script file, e.g. *configs/scripts/script.py*. 
   Only the variables which are defined in the *variable_list* property will be available from specified 
   nested script file under the namespace of the *var9* variable. ✨
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
6. Let's consider a couple of scenarios to demonstrate how variable referencing works. 🌅
   - First, you need to understand the difference between the *source* and *target* variables. Here, 
   *source* variable is the one whose reference is being used and *target* variable is the one that is 
   using the reference. 🎁🎁
   - ***Target* variable in the main config YAML file** : If the *target* variable is in the main config file, 
   such as *main.yaml*, then you can accomplish that in two ways depending on where the *source* 
   variable is.
     - **Source variable in the main config file** : If the *source* variable is in the main config 
     file, then use *$ref(SIBLING)* in the *target variable*. This will get the value from a variable 
     called *SIBLING* to the *target* variable like this. ✨
     ```yaml
     target_var:
       type: 'common'
       value: "$ref(SIBLING)"
     ```
     - **Source variable in a nested file** : If there is a *nested* variable called *nested1* and inside 
     the YAML of this file, there exists a variable called *varAA*, then the full *dot notation path* to this variable 
     from the main config file is *nested1.varAA*. So use *$ref(nested1.varAA)* in the *target variable*. ✨
     ```yaml
     target_var:
       type: 'common'
       value: "$ref(nested1.varAA)"
     ```
   - ***Target* variable in any other YAML/script file** : If the *target* variable is in any file other than 
   the main config file, then you can accomplish that in two ways depending on where the *source* variable is.
     - **Source variable in the same file** : If the *source* variable is in the same file as the  
     *target variable*, then use *$ref(SIBLING)* in the *target variable*. This will get the value from a variable 
     called *SIBLING* to the *target* variable like this. ✨
     ```yaml
     target_var:
       type: 'common'
       value: "$ref(SIBLING)"
     ```
     - **Source variable in any other file** : If there is a *nested* variable called *nested1* in the 
     main config file and inside the YAML of this *nested* variable, there exists a variable called 
     *varAA*, then the full *dot notation path* to this variable is *@.nested1.varAA*. 
     So use *$ref(@.nested1.varAA)* in the *target variable*. ✨
     ```yaml
     target_var:
       type: 'common'
       value: "$ref(@.nested1.varAA)"
     ```
   - **So, when to use *@* in the reference**: If the *target* variable is in the root config file, then you don't need 
   to add *@* in the full *dot notation path*. Because you can use the dotted path to follow the nested 
   variable hierarchy since you are already in the root config file. However, if the *target* variable 
   is in anywhere other than the root config file, then you need to prepend the *dot notation path* 
   with *@* to indicate whether to start looking for the *nested* variable from the root file or the 
   current file. Starting the dotted path with *@* simply means to *start looking for this variable 
   from the root config file*. 🎂🎂

NOTE: Referencing a variable is bidirectional and depth agnostic, meaning that any variable can be referenced 
**at any depth from any depth in any direction**, as long as no circular dependency is created during the 
referencing of another variable. *Circular Dependency* means that definitions of two variables are dependent 
on each other and neither variable can be resolved due to this dependency. In case of any circular dependency, 
confiGOAT will raise an exception indicating the circular dependency.

🌟🌟🌟

### Using Configuration Parameters in the Project

Now that you have prepared the configurations for your project, you need to use them in your project. 

1. First, you need to initialize and load all the configuration and environment variables.
   ```python3
   from configoat import conf
   conf.initialize(config="configs/main.yaml", env="dev", module="all_config")
   ```
   - *config* denotes the path to the main configuration YAML file to start loading the variables from.
   - *env* denotes which environment the variables should be loaded for.
   - *module* denotes the name of the namespace under which all variables will be made available for the 
   dynamic module access.
   - In practice, you don't want to hardcode the environment value like this, *env="dev"*. This way, you 
   won't be able to change it dynamically on the different environments your app is running on. We 
   recommend getting this value from another source that can be resolved during runtime. E.g. if you are 
   using confiGOAT in a Django app, then using CI/CD or starting script, inject the environment value 
   as the command line argument during the project run. Then, before initialization, 
   fetch this value from *os* like below,
   ```python3
   import os
   from configoat import conf
   current_env = os.getenv("YOUR_ENVIRONMENT_VARIABLE")
   conf.initialize(config="configs/main.yaml", env=current_env, module="all_config")
   ```
2. To access the configuration variables, you have 2 options.
   - *Dot notation* : You can use the *conf* object to access any variable by providing its full 
   *dot notation path* from the root configuration file. *@* denotes the root of the configuration, 
   i.e. the main configuration file. You can also pass the *conf* variable around like any other variable in python
   and access values like shown below.
   ```python3
   print(conf("@.VARIABLE_NAME"))
   print(conf("@.NESTED.VARIABLE_NAME"))
   
   print(conf.get("@.VARIABLE_NAME"))
   print(conf.get("@.NESTED.VARIABLE_NAME"))
   ```
   - *Dynamic module* : Use python's module and import mechanism to access any configuration 
   variable. In this approach, you import the module that you defined during the initialization step,
   e.g. *all_config*. When confiGOAT initialized your configuration variables, it also created dynamic 
   modules and attributes in those modules following your configuration nested hierarchy. All these 
   dynamic modules are inserted under the provided namespace, e.g. the *all_config* module name. After 
   initialization, you can import this module anywhere in your project and access the variables like any other modules 
   and their attributes. Some examples are given below on how variables can be accessed using dynamic module. 
   ```python3
   # accessing variables from the root module name, i.e. all_config
   import all_config
   print(all_config.var3)
   print(all_config.var2.var4)
   
   # importing all variables using * from the root module name, i.e. all_config
   from all_config import *
   print(var3)
   print(var2.var4)
   
   from all_config import var2 as current
   print(current.var4)
   ```

**You can also provide a default value in case the variable is not found and a casting function to transform
the final value before returning. Casting and default value features are available only when 
accessing values using *conf()* or *conf.get()***.
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



