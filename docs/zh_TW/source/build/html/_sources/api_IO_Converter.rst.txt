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

將 easy_config 實例轉換為其他常見的配置實例，反之亦然。
注意：轉換後的結果可能會有所不同，這取決於目標配置的支持情況。
例如，argparse 並未明確提供存儲層次結構配置的方法，因此轉換後的配置將會被扁平化(flatten)！

:raw-html-m2r:`<a id="IO_Converter.IO_Converter.__init__"></a>`

__init__
~~~~~~~~

.. code-block:: python

   def __init__()

轉換器的構造函數。在此，我們聲明了輸出/輸入分發器，用於將 easy_config 實例分派到指定的子程序中。

:raw-html-m2r:`<a id="IO_Converter.IO_Converter.cnvt_cfg_to"></a>`

cnvt_cfg_to
~~~~~~~~~~~

.. code-block:: python

   def cnvt_cfg_to(cfg, target_cfg_type: str, **cnvtr_kwarg)

將 easy_configer 轉換為其他常見配置實例。

**Arguments**\ :


* ``cfg`` *Configer* - easy_configer 實例。
* ``target_cfg_type`` *str* - 支持的配置類型的字符串標籤，可以通過 ``self.output_dispatcher.keys()`` 查看。
* ``cnvtr_kwarg`` ``**kwargs`` - 其他關鍵字參數，將嘗試傳遞給轉換子程序。

**Returns**\ :
   任何類型，目標配置實例。

:raw-html-m2r:`<a id="IO_Converter.IO_Converter.cnvt_cfg_from"></a>`

cnvt_cfg_from
~~~~~~~~~~~~~

.. code-block:: python

   def cnvt_cfg_from(other_cfg, target_cfg_type: str, **cnvtr_kwarg)

將給定的常見配置實例轉換為 easy_configer 。

**Arguments**\ :


* ``other_cfg`` *Any* - 任何支持的配置實例。
* ``target_cfg_type`` *str* - 支持的配置類型的字符串標籤，可以通過 ``self.input_dispatcher.keys()`` 查看。
* ``cnvtr_kwarg`` ``**kwargs`` - 其他關鍵字參數，將嘗試傳遞給轉換子程序。

**Returns**\ :
  Configer。
