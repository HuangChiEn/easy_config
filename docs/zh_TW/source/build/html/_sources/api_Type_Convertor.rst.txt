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

這個輔助類的目的是將配置字符串解析為對應類型的值。考慮到安全問題，我們避免使用 eval() 解析有害代碼。
相反，我們通過使用 ``ast.literal_eval()`` 限制了解析能力，因此可以放心使用默認的類型轉換器。

:raw-html-m2r:`<a id="utils.Type_Convertor.Type_Convertor.__init__"></a>`

__init__
~~~~~~~~

.. code-block:: python

   def __init__(typ_split_chr: str = '@', filter_split_chr: str = ' | ')

type convertor的建構子。

**Arguments**\ :


* 
  ``typ_split_chr`` *str, option* - 用於分隔配置文件中聲明字符串的字符。  
  例如，"a = 13@int" 表示參數 "a" 是整數類型數據，"@" 是 ``typ_split_chr``。默認為 ``@``。

* 
  ``filter_split_chr`` *str, option* - 用於分隔值字符串並確定解析後值的對應 "後處理" 函數的字符。  
  例如，``a = hello@str | upper``，其中 "upper" 後處理器會將 "a" 轉換為大寫字符串 "HELLO"。默認為 ``|``。

:raw-html-m2r:`<a id="utils.Type_Convertor.Type_Convertor.convert"></a>`

convert
~~~~~~~

.. code-block:: python

   def convert(cfg_raw_str: str, tmp_cfg_node=None)

**Arguments**\ :


* 
  ``cfg_raw_str`` *str* - 以與配置文件中相同語法聲明參數的字符串。

* 
  ``tmp_cfg_node`` *AttributeDict* - 用於插入參數的容器，存儲在配置中定義的所有參數。默認為 None。

:raw-html-m2r:`<a id="utils.Type_Convertor.Type_Convertor.regist_cnvtor"></a>`

regist_cnvtor
~~~~~~~~~~~~~

.. code-block:: python

   def regist_cnvtor(type_name: str = None, cnvt_func: callable = None)

註冊自定義類。

**Arguments**\ :


* 
  ``type_name`` *str* - 註冊的函數名稱，即自定義類的名稱。默認為 None。

* 
  ``cnvt_func`` *callable* - 用於將字符串對象轉換為自定義類實例的函數。默認為 None。

:raw-html-m2r:`<a id="utils.Type_Convertor.Type_Convertor.regist_filter"></a>`

regist_filter
~~~~~~~~~~~~~

.. code-block:: python

   def regist_filter(filter_name: str = None, filter_func: callable = None)

註冊後處理函數。

**Arguments**\ :


* 
  ``type_name`` *str* - 註冊函數的名稱，即自定義類的名稱。默認為 None。

* 
  ``cnvt_func`` *callable* - 用於將字符串對象轉換為自定義類實例的函數。默認為 None。
