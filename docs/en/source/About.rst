.. role:: raw-html-m2r(raw)
   :format: html


.. image:: assets/logo.png
   :target: assets/logo.png
   :alt: easy-configer logo


About this project
=====================

Preface ✨
^^^^^^^^^^^^

easy_configer version : 2.3.2

..

   Note : version 2.3.1 just a document fixup for pypi

Configeruating the program in an easy-way 

I'm willing to provide a light-weight solution for configurating your python program.
Hope this repository make every user control their large project with easier ~ ~ 

Introduction 📝
^^^^^^^^^^^^^^^^

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



That leverage me to package my solution for solving this issue. The easy_config will cover the following attributes :


#. 
   **Hierachical section config (nested dictionary)**

#. 
   **Accept multiple config file in dynamic loading manner**

#. 
   **Support customized class (initialized by keyword arguments)**

#. 
   **Commend-line update all declared-value wherever it belong, even in hierachical section**

#. 
   **Support the absl style FLAGS functionality (declare once, use anywhere)** 

And, of course the following attribute will also be supported :

* 
  dot-access of any arguments (even in nested dictionary)

* 
  inline comment '#', now you can write comment in everyline ~

* 
  support arguments interpolation!!

* 
  support config conversion, which turn easy_config into the other kind of config package (omegaconf, argparse, ..., etc.)

* 
  support hierachical configurating system with dynamic override ~
