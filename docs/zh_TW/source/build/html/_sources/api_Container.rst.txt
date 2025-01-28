.. role:: raw-html-m2r(raw)
   :format: html


utils.Container
=================


* `utils.Container <#utils.Container>`_

  * `AttributeDict <#utils.Container.AttributeDict>`_

    * `__init__ <#utils.Container.AttributeDict.\_\_init\_\_>`_
    * `__getattribute__ <#utils.Container.AttributeDict.\_\_getattribute\_\_>`_
    * `__getattr__ <#utils.Container.AttributeDict.\_\_getattr\_\_>`_
    * `set_attr_dict <#utils.Container.AttributeDict.set_attr_dict>`_
    * `__setattr__ <#utils.Container.AttributeDict.\_\_setattr\_\_>`_
    * `__setitem__ <#utils.Container.AttributeDict.\_\_setitem\_\_>`_
    * `__deepcopy__ <#utils.Container.AttributeDict.\_\_deepcopy\_\_>`_
    * `__getstate__ <#utils.Container.AttributeDict.\_\_getstate\_\_>`_
    * `__setstate__ <#utils.Container.AttributeDict.\_\_setstate\_\_>`_

  * `Flag <#utils.Container.Flag>`_

    * `__new__ <#utils.Container.Flag.\_\_new\_\_>`_
    * `FLAGS <#utils.Container.Flag.FLAGS>`_


:raw-html-m2r:`<a id="utils.Container.AttributeDict"></a>`

AttributeDict
--------------

.. code-block:: python

   class AttributeDict(dict)

這是一個類似字典的容器，用來存儲在配置中定義的嵌套參數。
由於該容器繼承自 Python 原生的字典（基類），我們以非常簡單的方式將參數存儲在基類字典中： ``dict[key] = value``，
通過在子類中調用 ``super().__setitem__(key, value)`` 實現。
此外，``self.__setattr__`` 也會在內部調用 ``super().__setitem__``！
根據我們存儲參數的方式，我們可以通過非常簡單的方式來訪問參數 ``self[key]``（即 dict[key]）。
另外，我們為實現 ``defaultdict`` 功能構建了 getattr 保護機制。``self.__getitem__`` 無需重寫，與基類相同。

:raw-html-m2r:`<a id="utils.Container.AttributeDict.__init__"></a>`

__init__
~~~~~~~~

.. code-block:: python

   def __init__(init_dict={})

Container 建構子。

**Arguments**\ :


* ``init_dict`` *dict* - 通常，它將是 Configer 中解析後的組態值字典。默認為空字典。

**Returns**\ :

  None.

:raw-html-m2r:`<a id="utils.Container.AttributeDict.__getattribute__"></a>`

__getattribute__
~~~~~~~~~~~~~~~~

.. code-block:: python

   def __getattribute__(attr)

覆寫 **getattribute** 魔術方法(dunder method)。
由於我們使用基類（dict）來存儲所有參數，因此不應該以任何方式使用 self.dict。

Raise:
    當用戶嘗試訪問 ``self.dict`` 時，將引發 Runtime Error。

:raw-html-m2r:`<a id="utils.Container.AttributeDict.__getattr__"></a>`

__getattr__
~~~~~~~~~~~

.. code-block:: python

   def __getattr__(key)

覆寫 **getattr** 魔術方法(dunder method)，以靜默方式構建 "空字典"。  
這樣，我們可以在不定義其父字典的情況下，將值分配給特定的參數。  
注意：與 ``defaultdict`` 相同的行為，允許遞歸地使用 ``self.__setattr__``。

**Returns**\ :

  AttributeDict, 返回的字典具有預定義的空字典，然後可以將特定參數更新到空字典中。

:raw-html-m2r:`<a id="utils.Container.AttributeDict.set_attr_dict"></a>`

set_attr_dict
~~~~~~~~~~~~~

.. code-block:: python

   def set_attr_dict(raw_dict)

將輸入的字典轉換為 AttributeDict 實例，並在內部調用 setitem 方法。

**Arguments**\ :


* ``raw_dict`` *dict* - Python 原生字典，調用此方法後將轉換為 AttributeDict 實例。

:raw-html-m2r:`<a id="utils.Container.AttributeDict.__setattr__"></a>`

__setattr__
~~~~~~~~~~~

.. code-block:: python

   def __setattr__(key, value)

覆寫 **setattr** 魔術方法(dunder method)，內部呼叫 **setitem** 方法。 

:raw-html-m2r:`<a id="utils.Container.AttributeDict.__setitem__"></a>`

__setitem__
~~~~~~~~~~~

.. code-block:: python

   def __setitem__(key, value)

覆寫 **setitem** 魔術方法(dunder method)，將任何輸入值包裝在 AttributeDict 容器中。 

:raw-html-m2r:`<a id="utils.Container.AttributeDict.__deepcopy__"></a>`

__deepcopy__
~~~~~~~~~~~~

.. code-block:: python

   def __deepcopy__(memo=None)

支持 deepcopy，參考連結:https://stackoverflow.com/questions/49901590/python-using-copy-deepcopy-on-dotdict。

:raw-html-m2r:`<a id="utils.Container.AttributeDict.__getstate__"></a>`

__getstate__
~~~~~~~~~~~~

.. code-block:: python

   def __getstate__()

基本的序列化接口（例如 pickle）。返回序列化的 Python 對象。

:raw-html-m2r:`<a id="utils.Container.AttributeDict.__setstate__"></a>`

__setstate__
~~~~~~~~~~~~

.. code-block:: python

   def __setstate__(de_ser_self)

基本的反序列化接口（例如 pickle）。接受反序列化的對象，並將其替換為默認的 self。

:raw-html-m2r:`<a id="utils.Container.Flag"></a>`

Flag
----

.. code-block:: python

   class Flag(object)

這是一個同步對象，用於在 Configer 中定義配置。它受到 TensorFlow 中 absl 旗標的啟發。
雖然這個類在目前並不常用，但我們保留了這個類以保持與 easy_config 早期版本的兼容性。
如果有必要，你仍然可以使用它。

:raw-html-m2r:`<a id="utils.Container.Flag.__new__"></a>`

__new__
~~~~~~~

.. code-block:: python

   def __new__(cls, *args, **kwargs)


覆寫 **new** 魔法方法。**new** 用於在調用 **init** 之前創建類的實例，因此我們在此處設置單例護衛(singleton guard)，以實現單例設計模式。

**Arguments**\ :

  `*args, **kwargs` : 將被傳遞給 FLAG_spec 實例，它是單例實例。

**Returns**\ :

  FLAG_spec，一個同步配置對象。

:raw-html-m2r:`<a id="utils.Container.Flag.FLAGS"></a>`

FLAGS
~~~~~

.. code-block:: python

   @property
   def FLAGS()

用於訪問 FLAG_spec 對象的介面。
