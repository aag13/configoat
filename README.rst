.. raw:: html

   <h1 align="center">

confiGOAT

.. raw:: html

   </h1>

confiGOAT is a powerful, flexible, and developer-friendly configuration
management tool.

Features:

-  Manage all your environment variables or configuration parameters
   from a single setup.
-  Use environment variables for different environments from the same
   setup.
-  Cast values before you use them.
-  Allow simple structure to configure nested configurations.
-  Load configuration parameters from python scripts.
-  Access parameters at every nested level using dynamic module.
-  Keep track of all parameters using a single interface.

Installing
----------

confiGOAT can be installed with `pip <https://pip.pypa.io>`__:

.. code:: bash

   $ pip install configoat

Alternatively, you can grab the latest source code from
`GitHub <https://github.com/aag13/configoat>`__:

.. code:: bash

   $ git clone https://github.com/aag13/configoat
   $ cd configoat
   $ pip install .

configoat is powerful and easy to use:

You can initialize the package using the following management command.

.. code:: bash

   $ configoat init

How to Use confiGOAT
--------------------

Access environment variables using get() inside any python module/script

.. code:: python3

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

Access environment variables using dynamic modules inside any python
module/script

.. code:: python3

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

Documentation
-------------

confiGOAT has usage and reference documentation at
`confiGOAT.readthedocs.io <https://github.com/aag13/configoat/blob/main/README.rst>`__.

Contributing
------------

confiGOAT happily accepts contributions. Please see our `contributing
documentation <https://github.com/aag13/configoat/blob/main/CONTRIBUTING.rst>`__
for some tips on getting started.

Maintainers
-----------

-  `@banna <https://github.com/Hasan-Ul-Banna>`__ (Hasan-UL-Banna)
-  `@galib <https://github.com/aag13>`__ (Asadullah Al Galib)

👋
