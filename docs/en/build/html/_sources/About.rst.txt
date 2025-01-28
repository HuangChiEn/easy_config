.. role:: raw-html-m2r(raw)
   :format: html


.. image:: assets/logo.png
   :target: assets/logo.png
   :alt: easy-configer logo


About this project
=====================

🚧 TODO list :
^^^^^^^^^^^^^^^^^^
#.
   Release known issue area in v2.5.6 and hot-fix in v2.6.

#. 
   Tag v2.6 as stable version.

#.
   Next version v3.0 is under development, stateless interface will be introduced as one of new features

#.
   Nested argument intepolation may be one of features in v3.0

#. 
   You can preview the v3.0 prototype of codebase under ./dev folder 


🐞 Known issues : 
^^^^^^^^^^^^^^^^^^^

#.
   allow_overwrite flag also allow you overwrite the entire section by a config value, most of case it should not a expected behavior (pitfall)

#.
   Commendline argument CAN NOT update the arguments in sub_config (bug)

----

Preface ✨
^^^^^^^^^^^^

easy_configer version : 2.5.6

Configeruating the program in an easy-way 

I'm willing to provide a light-weight solution for configurating your python program.
Hope this repository make every user control their large project with easier ~ ~ 

Introduction 📝
^^^^^^^^^^^^^^^^

🙋‍♂️ Why choice easy_configer ?
"""""""""""""""""""""""""""""""""

With the python project go into large-scale, a lot of argument will be required to control the complex business logic, user may need a simple way to load configurations through a file eventually. Their exists various package cover part of function and offer some solution to tackle the mentioned problem. 

**Unfortunately, I can not find a solution for load & use the argument in simple manner at least.**   Instead, most of the config-tools seems only works for the specific goal, then cause the code more longer and hard to read.

For example :

.. code-block:: python

   ## ConfigParser
   import ConfigParser 
   Config = ConfigParser.ConfigParser()
   Config.read("c:\\tomorrow.ini")
   # get arg via method
   Config.get(section, option)
   # or get arg with converter
   int(Config['lucky_num'])

   ## Argparse
   import argparse
   parse = argparse.ArgumentParser("description string")
   parse.add_argument("--lucky_num", type=int)
   ...
   args = parser.parse_args()
   args.lucky_num

   ## Omegaconf
   from omegaconf import OmegaConf
   conf = OmegaConf.load('source/example.yaml')
   conf.player.height

Except omegaconf, most of config tools have much redundant syntax to load and access config arguments. 
However, omegaconf also have several draw backs : 

#. 
   Too much dependencies (version competible may become issue!)

#. 
   Dynamic config loading system is hard to trace (which config overwrite my default setup ?)

#. 
   Non-native container (it apply Mappable object, so need to apply to_container for further convertion)

That leverage me to package my solution for solving those issue. easy_configer have several advantages :

#. 
   Zero-dependency!! (except you want to convert easy_configer to other config tools instance)

#. 
   Flexible apply :code:`allow_overwrite=False`, you can easily detect the overwritted arguments..

#. 
   Our container inherit pure python dict! Most of dict methods are also online ~

My solution also cover the following attributes :

#. 
   **Hierachical section config (nested dict-like config)**

#. 
   **Accept multiple config file in dynamic loading manner (similar with omegaconf)**

#. 
   **Support customized class (initialized by list or keyword arguments)**

#. 
   **Commend-line add/update declared arguments/sections (even in hierachical section)**

#. 
   **Support the absl style FLAGS functionality (declare once, use anywhere)** 

And, of course the following attribute will also be supported :

* 
  dot-access of any arguments (even in nested dictionary)

* 
  inline comment '#', now you can write comment in everyline ~

* 
  support config argument interpolation (even in nested dictionary)!

* 
  support config conversion, feel free to use easy_config or the other config tools (omegaconf, argparse, ..., etc.)

* 
  support omegaconf-like dynamic config loading system ~
