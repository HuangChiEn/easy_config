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

easy_configer中實現使用者組態的核心模組。

:raw-html-m2r:`<a id="Configer.Configer.__init__"></a>`

__init__
~~~~~~~~

.. code-block:: python

   def __init__(description: str = "",
                cmd_args: bool = False,
                split_chr: str = " = ") -> None

Configer的建構子。

**Arguments**\ :

* ``description`` *str, optional* - 自定義的幫助信息，用於描述配置文件的作用。默認為空字符串。
* ``cmd_args`` *bool, optional* - 一個旗標，用於指示是否從命令行讀取參數並覆蓋默認配置。默認為 False。
* ``split_chr`` *str, optional* - 用於格式化配置語法的字符字符串。默認為 " = "。
  例如，"a\*13@int" 表示參數 'a' 包含整數值 13，並且 "*" 是組態剖析的分割字元。
  請注意，最好不要更改分割字元以防止符號衝突。

**Returns**\ :

  None. 構造函數不接受任何返回值。

:raw-html-m2r:`<a id="Configer.Configer.cfg_from_cli"></a>`

cfg_from_cli
~~~~~~~~~~~~

.. code-block:: python

   def cfg_from_cli() -> None

從命令行輸入構建配置，並僅應用來自命令行的參數。
（僅推薦用於非常輕量級的配置）

:raw-html-m2r:`<a id="Configer.Configer.cfg_from_str"></a>`

cfg_from_str
~~~~~~~~~~~~

.. code-block:: python

   def cfg_from_str(raw_cfg_text: str, allow_override: bool = False) -> None

從給定的配置字符串構建配置。

**Arguments**\ :


* ``raw_cfg_text`` *str* - 用於聲明參數的字符串，語法與配置文件中使用的語法相同。
* ``allow_override`` *bool, optional* - 一個旗標，允許從其他來源覆蓋配置，例如其他 .ini 配置文件或配置字符串。默認為 False。

:raw-html-m2r:`<a id="Configer.Configer.cfg_from_ini"></a>`

cfg_from_ini
~~~~~~~~~~~~

.. code-block:: python

   def cfg_from_ini(cfg_path: str, allow_override: bool = False) -> None

從給定 .ini 組態檔中建構配置。

**Arguments**\ :


* ``cfg_path`` *str* - 配置文件的路徑，指向 *.ini* 配置文件。
* ``allow_override`` *bool, optional* - 一個旗標，允許從其他來源覆蓋配置，例如其他 .ini 配置文件或配置字符串。默認為 False。

:raw-html-m2r:`<a id="Configer.Configer.args_from_cmd"></a>`

args_from_cmd
~~~~~~~~~~~~~

.. code-block:: python

   def args_from_cmd() -> None

通過命令行輸入字符串更新參數。
請注意，這個方法允許原生地覆蓋預定義的配置（以靜默模式進行）。
（由於命令行輸入是由用戶明確給出的，因此我們不需要發出警告。）

:raw-html-m2r:`<a id="Configer.Configer.__or__"></a>`

__or__
~~~~~~

.. code-block:: python

   def __or__(cfg)

支持將兩個配置進行合併，並“覆蓋”左側配置。
例如，cfg_a = cfg_a | cfg_b，此時 cfg_a 將被 cfg_b 覆蓋。

**Arguments**\ :


* ``cfg`` *AttributeDict* - 用來存儲參數的容器。它繼承自字典，並且給定的輸入可以是嵌套的字典。

:raw-html-m2r:`<a id="Configer.Configer.__add__"></a>`

__add__
~~~~~~~

.. code-block:: python

   def __add__(cfg)

支持合併兩個配置，且不覆蓋任何配置。  
這個方法在內部調用 self.concate_cfg(.)。

**Arguments**\ :


* 
  ``cfg`` *AttributeDict* - 容器，用於存儲參數。它繼承自 dict，且給定的輸入可以是嵌套字典。

  Raise:
  當參數被重新定義時，會引發RuntimeError。

:raw-html-m2r:`<a id="Configer.Configer.concate_cfg"></a>`

concate_cfg
~~~~~~~~~~~

.. code-block:: python

   def concate_cfg(cfg)

支持合併兩個配置，且不會覆蓋任何配置。

**Arguments**\ :


* 
  ``cfg`` *AttributeDict* - 用於存儲參數的容器。它繼承自 dict，且給定的輸入可以是嵌套的字典。

  Raise:
  當參數被重新定義時，會引發 RuntimeError。

**Returns**\ :

  Configer。

:raw-html-m2r:`<a id="Configer.Configer.merge_conf"></a>`

merge_conf
~~~~~~~~~~

.. code-block:: python

   def merge_conf(cfg, override=True)

支持將兩個配置進行合併，並覆蓋配置。配置將被給定的 cfg 覆蓋。

**Arguments**\ :


* ``cfg`` *AttributeDict* - 用於存儲參數的容器。它繼承自 dict，且給定的輸入可以是嵌套的字典。
* ``override`` *bool* - 一個旗標，用於指示是否覆蓋配置的值，默認為 True。

**Returns**\ :

  None. 這是 inplace 操作。

:raw-html-m2r:`<a id="Configer.Configer.__str__"></a>`

__str__
~~~~~~~

.. code-block:: python

   def __str__()

展示配置中所有 “非私有” 的參數。

:raw-html-m2r:`<a id="Configer.Configer.__iter__"></a>`

__iter__
~~~~~~~~

.. code-block:: python

   def __iter__()

Return Configer 的迭代器。由於 Configer 本身不是字典，因此需要此方法。

:raw-html-m2r:`<a id="Configer.Configer.__getitem__"></a>`

__getitem__
~~~~~~~~~~~

.. code-block:: python

   def __getitem__(key)

支持 getitem 操作。由於 Configer 本身不是字典，因此需要此方法。

:raw-html-m2r:`<a id="Configer.Configer.__setitem__"></a>`

__setitem__
~~~~~~~~~~~

.. code-block:: python

   def __setitem__(key, value)

支持 setitem 操作。由於 Configer 本身不是字典，因此需要此方法。

:raw-html-m2r:`<a id="Configer.Configer.get"></a>`

get
~~~

.. code-block:: python

   def get(key, default_value=None)

支持 get 操作。由於 Configer 本身不是字典，因此需要此方法。

:raw-html-m2r:`<a id="Configer.Configer.get_cfg_flag"></a>`

get_cfg_flag
~~~~~~~~~~~~

.. code-block:: python

   def get_cfg_flag()

Return 同步配置的 FLAG 物件。

:raw-html-m2r:`<a id="Configer.Configer.get_doc_str"></a>`

get_doc_str
~~~~~~~~~~~

.. code-block:: python

   def get_doc_str()

Return 幫助信息字符串。

:raw-html-m2r:`<a id="Configer.Configer.regist_cnvtor"></a>`

regist_cnvtor
~~~~~~~~~~~~~

.. code-block:: python

   def regist_cnvtor(type_name: str = None, cnvt_func: callable = None)

聲明用戶自定義的類型。註冊的類型（類）可用於配置文件中參數的聲明。

**Arguments**\ :


* 
  ``type_name`` *str* - 配置文件中使用的類型名稱。例如註冊為 'dummy'，則聲明此類型的參數應該是 ``var = {'arg1':42}@dummy``。

* 
  ``cnvt_func`` *callable* - 通常是自定義類的構造函數。所以，你可以直接將自定義類作為這個參數提供。

**Returns**\ :

  None. 此註冊方法不返回任何旗標。

:raw-html-m2r:`<a id="Configer.Configer.split_char"></a>`

split_char
~~~~~~~~~~

.. code-block:: python

   @property
   def split_char()

顯示配置文件中使用的分割字元。
