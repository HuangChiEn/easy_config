.. role:: raw-html-m2r(raw)
   :format: html

Installation
=============


How to install ? ⚙️\ :raw-html-m2r:`<br>`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. **pypi install** :raw-html-m2r:`<br>`
    simply type the ``pip install easy_configer`` (due to name conflict of pypi pkg, we use different pkg name)
#. **install from source code** :raw-html-m2r:`<br>`
    clone the project from github : ``git clone https://github.com/HuangChiEn/easy_config.git`` 
    Chage to the root directory of the cloned project, and type ``pip install -e .``
#. **import syntax** :raw-html-m2r:`<br>`
     Wherever you install, pypi or source. Now, you just need a simple import : ``from easy_configer.Configer import Configer``

----

Dependencies 🏗️
^^^^^^^^^^^^^^^^^^

This package is written for Python 3.8 (but 3.6+ may be supported).
Of course, light-weight solution **do not** contain any 3-rd package complex dependencies.
The python standard package (such as pathlib, sys, .., etc) is the only source of dependencies, so you don't need to worry about that ~ ~

..

   However, if you want to use the IO_Converter for converting config into omegaconf, you still need to install omegaconf for this functionality ~
