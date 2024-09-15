.. role:: raw-html-m2r(raw)
   :format: html


utils.Type_Convertor
======================


* `utils.Type_Convertor <#utils.Type_Convertor>`_

  * `Type_Convertor <#utils.Type_Convertor.Type_Convertor>`_

    * `__init__ <#utils.Type_Convertor.Type_Convertor.\_\_init\_\_>`_
    * `convert <#utils.Type_Convertor.Type_Convertor.convert>`_
    * `regist_cnvtor <#utils.Type_Convertor.Type_Convertor.regist_cnvtor>`_
    * `regist_filter <#utils.Type_Convertor.Type_Convertor.regist_filter>`_


:raw-html-m2r:`<a id="utils.Type_Convertor.Type_Convertor"></a>`

Type_Convertor
--------------

.. code-block:: python

   class Type_Convertor(object)

This helper class aims to parse the config string into
the value of the corresponding type. Concerning security issue, we prevent to parse the harmful code by using eval(.). Instead, we constraint the parse capability by using ast.literal_eval(.), so feel free to use the default type converter.

:raw-html-m2r:`<a id="utils.Type_Convertor.Type_Convertor.__init__"></a>`

__init__
~~~~~~~~

.. code-block:: python

   def __init__(typ_split_chr: str = '@', filter_split_chr: str = ' | ')

Constructor of type convertor.

**Arguments**\ :


* 
  ``typ_split_chr`` *str, option* - The character is used to split the declaration string in configer file.
  For example, 'a = 13@int' which means the argument 'a' is interger type data, and the '@' is the typ_split_chr. Default to ``@``.

* 
  ``filter_split_chr`` *str, option* - The character is used to split the value string and figure out the corresponding 'post-process' for the parsed value. For example,
  'a = hello@str | upper', the upper post-processor will turn a into HELLO string.
  Default to ``|``.

:raw-html-m2r:`<a id="utils.Type_Convertor.Type_Convertor.convert"></a>`

convert
~~~~~~~

.. code-block:: python

   def convert(cfg_raw_str: str, tmp_cfg_node=None)

**Arguments**\ :


* 
  ``cfg_raw_str`` *str* - The string which declare the arguments with the same syntax used in config file.

* 
  ``tmp_cfg_node`` *AttributeDict* - The container, which is used to intepolate the argument, store all arguments defined in config.
  Default to None.

:raw-html-m2r:`<a id="utils.Type_Convertor.Type_Convertor.regist_cnvtor"></a>`

regist_cnvtor
~~~~~~~~~~~~~

.. code-block:: python

   def regist_cnvtor(type_name: str = None, cnvt_func: callable = None)

Regist the customized class.

**Arguments**\ :


* 
  ``type_name`` *str* - Name of registered function, namely the name of customized class. Default to None.

* 
  ``cnvt_func`` *callable* - The function for converting the string object into the customized class instance. Default to None.

:raw-html-m2r:`<a id="utils.Type_Convertor.Type_Convertor.regist_filter"></a>`

regist_filter
~~~~~~~~~~~~~

.. code-block:: python

   def regist_filter(filter_name: str = None, filter_func: callable = None)

Regist the postprocessing function.

**Arguments**\ :


* 
  ``type_name`` *str* - Name of registered function, namely the name of customized class. Default to None.

* 
  ``cnvt_func`` *callable* - The function for converting the string object into the customized class instance. Default to None.
