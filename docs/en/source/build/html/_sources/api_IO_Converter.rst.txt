.. role:: raw-html-m2r(raw)
   :format: html


IO_Converter
==============


* `IO_Converter <#IO_Converter.IO_Converter>`_

   * `__init__ <#IO_Converter.IO_Converter.\_\_init\_\_>`_
   * `cnvt_cfg_to <#IO_Converter.IO_Converter.cnvt_cfg_to>`_
   * `cnvt_cfg_from <#IO_Converter.IO_Converter.cnvt_cfg_from>`_

:raw-html-m2r:`<a id="IO_Converter.IO_Converter"></a>`

IO_Converter
------------

.. code-block:: python

   class IO_Converter(object)

The interface to convert easy_config instance to 'other common config' instance, and vice versa.
Note : the converted results may be slightly different according to the support of target config.
For example, argparse doesn't explicitly provide a way for storing hierachical config, so the converted 
config will be flattened!

:raw-html-m2r:`<a id="IO_Converter.IO_Converter.__init__"></a>`

__init__
~~~~~~~~

.. code-block:: python

   def __init__()

Constructor of converter. In here, we declare the output/input dispatcher to 
dispatch the easy_config instance into the indicated subroutine.

:raw-html-m2r:`<a id="IO_Converter.IO_Converter.cnvt_cfg_to"></a>`

cnvt_cfg_to
~~~~~~~~~~~

.. code-block:: python

   def cnvt_cfg_to(cfg, target_cfg_type: str, **cnvtr_kwarg)

Convert easy_configer 'to' the other common config instance.

**Arguments**\ :


* ``cfg`` *Configer* - Easy_configer instance.
* ``target_cfg_type`` *str* - A string tag of supported config type. It could be viewed by ``self.output_dispatcher.keys()``.
* ``cnvtr_kwarg`` \*\*kwargs - Other keyword arguments attempt to pass to converter subroutine.

**Returns**\ :
   Any, the target config instance.

:raw-html-m2r:`<a id="IO_Converter.IO_Converter.cnvt_cfg_from"></a>`

cnvt_cfg_from
~~~~~~~~~~~~~

.. code-block:: python

   def cnvt_cfg_from(other_cfg, target_cfg_type: str, **cnvtr_kwarg)

Convert to easy_configer 'from' the given common config instance.

**Arguments**\ :


* ``other_cfg`` *Any* - Any supported config instance.
* ``target_cfg_type`` *str* - A string tag of supported config type. It could be viewed by ``self.input_dispatcher.keys()``.
* ``cnvtr_kwarg`` \*\*kwargs - Other keyword arguments attempt to pass to converter subroutine.

**Returns**\ :
  Configer.
