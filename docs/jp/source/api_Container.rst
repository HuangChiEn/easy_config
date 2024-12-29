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

設定で定義されたネストされた引数を格納するための辞書のようなコンテナです。
このコンテナは Python のネイティブ dict（基底クラス）を継承しているため、引数は基本的な辞書の方法で格納されます。
具体的には、``dict[key] = value`` という方法で格納され、サブクラス内で ``super().__setitem__(key, value)`` を呼び出します。
また、``self.__setattr__`` も内部で ``super().__setitem__`` を呼び出します。
引数を格納する方法に基づき、引数には ``self[key]``（つまり、dict[key]）でアクセスできます。
さらに、``getattr`` ガードを構築して、``defaultdict`` 機能を実装します。
``self.__getitem__`` はオーバーライドする必要はありません、基本クラスと同じ動作をします。

:raw-html-m2r:`<a id="utils.Container.AttributeDict.__init__"></a>`

__init__
~~~~~~~~

.. code-block:: python

   def __init__(init_dict={})

コンテナのコンストラクタ。

**Arguments**\ :


* ``init_dict`` *dict* - 通常は Configer で解析された値の辞書。デフォルトは空の辞書。

**Returns**\ :

  None.

:raw-html-m2r:`<a id="utils.Container.AttributeDict.__getattribute__"></a>`

__getattribute__
~~~~~~~~~~~~~~~~

.. code-block:: python

   def __getattribute__(attr)

**getattribute** の dunder メソッドをオーバーライドします。
基本クラス（dict）を引数を格納するために使用しているため、``self.__dict__`` は使用しないようにします。

Raise:
    ユーザーが ``self.__dict__`` にアクセスしようとした場合、``RuntimeError`` を発生させます。

:raw-html-m2r:`<a id="utils.Container.AttributeDict.__getattr__"></a>`

__getattr__
~~~~~~~~~~~

.. code-block:: python

   def __getattr__(key)

**getattr** の dunder メソッドをオーバーライドし、「空の辞書」を静かに構築します。
これにより、親辞書を定義せずに特定の引数に値を割り当てることができます。
``defaultdict`` と同様の動作を提供し、再帰的に ``self.__setattr__`` を許可します。

**Returns**\ :

  AttributeDict, 空の辞書を持つ事前定義された辞書が返され、その後特定の引数を更新できます。

:raw-html-m2r:`<a id="utils.Container.AttributeDict.set_attr_dict"></a>`

set_attr_dict
~~~~~~~~~~~~~

.. code-block:: python

   def set_attr_dict(raw_dict)

入力された辞書を AttributeDict インスタンスに変換し、内部で ``__setitem__`` を呼び出します。

**Arguments**\ :


* ``raw_dict`` *dict* -  Python のネイティブ辞書。これが AttributeDict に変換されます。

:raw-html-m2r:`<a id="utils.Container.AttributeDict.__setattr__"></a>`

__setattr__
~~~~~~~~~~~

.. code-block:: python

   def __setattr__(key, value)

**setattr** の dunder メソッドをオーバーライドし、内部で ``__setitem__`` を呼び出します。

:raw-html-m2r:`<a id="utils.Container.AttributeDict.__setitem__"></a>`

__setitem__
~~~~~~~~~~~

.. code-block:: python

   def __setitem__(key, value)

**setitem** の dunder メソッドをオーバーライドし、入力された値を AttributeDict コンテナでラップします。

:raw-html-m2r:`<a id="utils.Container.AttributeDict.__deepcopy__"></a>`

__deepcopy__
~~~~~~~~~~~~

.. code-block:: python

   def __deepcopy__(memo=None)

deepcopy をサポートします。詳細：https://stackoverflow.com/questions/49901590/python-using-copy-deepcopy-on-dotdict。

:raw-html-m2r:`<a id="utils.Container.AttributeDict.__getstate__"></a>`

__getstate__
~~~~~~~~~~~~

.. code-block:: python

   def __getstate__()

基本的なシリアライズインターフェース（例えば、pickle）を提供します。シリアライズされた Python オブジェクトを返します。

:raw-html-m2r:`<a id="utils.Container.AttributeDict.__setstate__"></a>`

__setstate__
~~~~~~~~~~~~

.. code-block:: python

   def __setstate__(de_ser_self)

基本的なシリアライズインターフェース（例えば、pickle）を提供します。デシリアライズされたオブジェクトを受け取り、デフォルトの self をそれに置き換えます。

:raw-html-m2r:`<a id="utils.Container.Flag"></a>`

Flag
----

.. code-block:: python

   class Flag(object)

Configer 内で設定を定義するための同期オブジェクトです。TensorFlow の absl flag に触発されています。
これは役立たないかもしれませんが、easy_config の初期バージョンとの互換性のためにこのクラスを保持しています。
それでも使用することができます。

:raw-html-m2r:`<a id="utils.Container.Flag.__new__"></a>`

__new__
~~~~~~~

.. code-block:: python

   def __new__(cls, *args, **kwargs)

new の dunder メソッドをオーバーライドします。new はクラスを作成するために init を呼び出す前に使用されます。
ここでシングルトンのガードを設定し、シングルトンデザインパターンを実装します。

**Arguments**\ :

  `*args, **kwargs` : インスタンス（シングルトンインスタンス）に渡されます。

**Returns**\ :

  FLAG_spec, 設定の同期オブジェクト。

:raw-html-m2r:`<a id="utils.Container.Flag.FLAGS"></a>`

FLAGS
~~~~~

.. code-block:: python

   @property
   def FLAGS()

FLAG_spec オブジェクトにアクセスするためのインターフェース。