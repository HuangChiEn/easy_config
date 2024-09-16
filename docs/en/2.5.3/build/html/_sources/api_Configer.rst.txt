.. role:: raw-html-m2r(raw)
   :format: html


Configer 
=========

* `Configer.Configer <#Configer.Configer>`_

   * `__init__ <#Configer.Configer.\_\_init\_\_>`_
   * `cfg_from_cli <#Configer.Configer.cfg_from_cli>`_
   * `cfg_from_str <#Configer.Configer.cfg_from_str>`_
   * `cfg_from_ini <#Configer.Configer.cfg_from_ini>`_
   * `args_from_cmd <#Configer.Configer.args_from_cmd>`_
   * `__or__ <#Configer.Configer.\_\_or\_\_>`_
   * `__add__ <#Configer.Configer.\_\_add\_\_>`_
   * `concate_cfg <#Configer.Configer.concate_cfg>`_
   * `merge_conf <#Configer.Configer.merge_conf>`_
   * `__str__ <#Configer.Configer.\_\_str\_\_>`_
   * `__iter__ <#Configer.Configer.\_\_iter\_\_>`_
   * `__getitem__ <#Configer.Configer.\_\_getitem\_\_>`_
   * `__setitem__ <#Configer.Configer.\_\_setitem\_\_>`_
   * `get <#Configer.Configer.get>`_
   * `get_cfg_flag <#Configer.Configer.get_cfg_flag>`_
   * `get_doc_str <#Configer.Configer.get_doc_str>`_
   * `regist_cnvtor <#Configer.Configer.regist_cnvtor>`_
   * `split_char <#Configer.Configer.split_char>`_

:raw-html-m2r:`<a id="Configer.Configer"></a>`

Configer
----------

.. code-block:: python

   class Configer(object)

The core module of easy_configer to implement the user configuration system.

:raw-html-m2r:`<a id="Configer.Configer.__init__"></a>`

__init__
~~~~~~~~

.. code-block:: python

   def __init__(description: str = "",
                cmd_args: bool = False,
                split_chr: str = " = ") -> None

Constructor of Configer.

**Arguments**\ :


* ``description`` *str, optional* - A customized helper information which describe the role of config file. Defaults to empty string.
* ``cmd_args`` *bool, optional* - A flag to indicate reading argument from commendline and override the default config. Defaults to False.
* ``split_chr`` *str, optional* - A char-string used to format the config syntax. Defaults to " = ".
  For example, "a\*13@int" which means the argument 'a' contain interger value 13,
  and the "*" is the split_chr.
  Note that better not to change this char-string to prevent the symbol conflict.

**Returns**\ :

  None. Don't accept anything return from constructor.

:raw-html-m2r:`<a id="Configer.Configer.cfg_from_cli"></a>`

cfg_from_cli
~~~~~~~~~~~~

.. code-block:: python

   def cfg_from_cli() -> None

Building config from the commendline input and only apply the arguments from commend-line.
( only recommend for very lightweight config )

:raw-html-m2r:`<a id="Configer.Configer.cfg_from_str"></a>`

cfg_from_str
~~~~~~~~~~~~

.. code-block:: python

   def cfg_from_str(raw_cfg_text: str, allow_override: bool = False) -> None

Building config from the given config string.

**Arguments**\ :


* ``raw_cfg_text`` *str* - The string which declare the arguments with the same syntax used in config file.
* ``allow_override`` *bool, optional* - A flag allow override config from the other source,
  such as the other .ini config file, config string. Default to False.

:raw-html-m2r:`<a id="Configer.Configer.cfg_from_ini"></a>`

cfg_from_ini
~~~~~~~~~~~~

.. code-block:: python

   def cfg_from_ini(cfg_path: str, allow_override: bool = False) -> None

Building config from the given .ini config file.

**Arguments**\ :


* ``cfg_path`` *str* - The path which locate the *.ini* config file.
* ``allow_override`` *bool, optional* - A flag allow override config from the other source,
  such as the other .ini config file, config string. Default to False.

:raw-html-m2r:`<a id="Configer.Configer.args_from_cmd"></a>`

args_from_cmd
~~~~~~~~~~~~~

.. code-block:: python

   def args_from_cmd() -> None

Update the arguments by commend line input string.
Note that this method allow override the pre-define config natively (with silent mode).
( Because commentline inputs are explicitly given by user, we don't need to warn that )

:raw-html-m2r:`<a id="Configer.Configer.__or__"></a>`

__or__
~~~~~~

.. code-block:: python

   def __or__(cfg)

Support merge two config 'with override' the left-hand side config.
For example. cfg_a = cfg_a | cfg_b, cfg_a will be overrided by cfg_b.

**Arguments**\ :


* ``cfg`` *AttributeDict* - A container used to store the argument. it inherit from dict and the given input could be a nested dict.

:raw-html-m2r:`<a id="Configer.Configer.__add__"></a>`

__add__
~~~~~~~

.. code-block:: python

   def __add__(cfg)

Support merge two config 'without override' the any config.
This method call self.concate_cfg(.) underhood.

**Arguments**\ :


* 
  ``cfg`` *AttributeDict* - A container used to store the argument. it inherit from dict and the given input could be a nested dict.

  Raise:
  RuntimeError with re-define argument.

:raw-html-m2r:`<a id="Configer.Configer.concate_cfg"></a>`

concate_cfg
~~~~~~~~~~~

.. code-block:: python

   def concate_cfg(cfg)

Merge two config 'without override' the any config.

**Arguments**\ :


* 
  ``cfg`` *AttributeDict* - A container used to store the argument. it inherit from dict and the given input could be a nested dict.

  Raise:
  RuntimeError with re-define argument.

**Returns**\ :

  Configer.

:raw-html-m2r:`<a id="Configer.Configer.merge_conf"></a>`

merge_conf
~~~~~~~~~~

.. code-block:: python

   def merge_conf(cfg, override=True)

Merge two config 'with override' the config. The config will be overrided
by the given config cfg.

**Arguments**\ :


* ``cfg`` *AttributeDict* - A container used to store the argument. it inherit from dict and the given input could be a nested dict.
* ``override`` *bool* - A flag to indicate overriding value by the given config cfg. Default to True.

**Returns**\ :

  None. This is inplace operation.

:raw-html-m2r:`<a id="Configer.Configer.__str__"></a>`

__str__
~~~~~~~

.. code-block:: python

   def __str__()

Present all 'non-private' arguments defined in config.

:raw-html-m2r:`<a id="Configer.Configer.__iter__"></a>`

__iter__
~~~~~~~~

.. code-block:: python

   def __iter__()

Return iterator for Configer. Because Configer itself isn't dict.

:raw-html-m2r:`<a id="Configer.Configer.__getitem__"></a>`

__getitem__
~~~~~~~~~~~

.. code-block:: python

   def __getitem__(key)

Support getitem for Configer. Because Configer itself isn't dict.

:raw-html-m2r:`<a id="Configer.Configer.__setitem__"></a>`

__setitem__
~~~~~~~~~~~

.. code-block:: python

   def __setitem__(key, value)

Support setitem for Configer. Because Configer itself isn't dict.

:raw-html-m2r:`<a id="Configer.Configer.get"></a>`

get
~~~

.. code-block:: python

   def get(key, default_value=None)

Support get for Configer. Because Configer itself isn't dict.

:raw-html-m2r:`<a id="Configer.Configer.get_cfg_flag"></a>`

get_cfg_flag
~~~~~~~~~~~~

.. code-block:: python

   def get_cfg_flag()

Return the FLAG object which 'sync' the config.

:raw-html-m2r:`<a id="Configer.Configer.get_doc_str"></a>`

get_doc_str
~~~~~~~~~~~

.. code-block:: python

   def get_doc_str()

Return the helper information string.

:raw-html-m2r:`<a id="Configer.Configer.regist_cnvtor"></a>`

regist_cnvtor
~~~~~~~~~~~~~

.. code-block:: python

   def regist_cnvtor(type_name: str = None, cnvt_func: callable = None)

Declare the user customized class. The registered type (class) can be used
to declare the argument in the config file.

**Arguments**\ :


* 
  ``type_name`` *str* - type name used in config file. i.e. registered as 'dummy',
  then declare a argument with such type will be ``var = {'arg1':42}@dummy``.

* 
  ``cnvt_func`` *callable* - typically it's the constructor of your customized class.
  So, you can just directly feed the customized class as this arguemnt.

**Returns**\ :

  None. This registered method doesn't return any flag.

:raw-html-m2r:`<a id="Configer.Configer.split_char"></a>`

split_char
~~~~~~~~~~

.. code-block:: python

   @property
   def split_char()

Show the split char used in config file.
