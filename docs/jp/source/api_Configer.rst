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

easy_configer のコアモジュールは、ユーザー設定システムを実装するためのものです。

:raw-html-m2r:`<a id="Configer.Configer.__init__"></a>`

__init__
~~~~~~~~

.. code-block:: python

   def __init__(description: str = "",
                cmd_args: bool = False,
                split_chr: str = " = ") -> None

Configer のコンストラクタ。

**Arguments**\ :


* ``description`` *str, optional* - 設定コンフィグの役割を説明するカスタマイズされたヘルパー情報。デフォルトは空文字列です。
* ``cmd_args`` *bool, optional* - コマンドラインから引数を読み取り、デフォルト設定を上書きするフラグ。デフォルトは ``False`` です。
* ``split_chr`` *str, optional* - 設定構文をフォーマットするために使用される文字列。デフォルトは " = " です。例えば、"a*13@int" の場合、引数 'a' は整数値 13 を含み、* が split_chr です。この文字列を変更しない方が、シンボルの競合を避けるために推奨されます。

**Returns**\ :

  None. コンストラクタは何も返しません。

:raw-html-m2r:`<a id="Configer.Configer.cfg_from_cli"></a>`

cfg_from_cli
~~~~~~~~~~~~

.. code-block:: python

   def cfg_from_cli() -> None

コマンドライン入力のみ設定を構築し、コマンドライン引数のみを適用します。
（非常に軽量な設定の場合にのみ推奨）

:raw-html-m2r:`<a id="Configer.Configer.cfg_from_str"></a>`

cfg_from_str
~~~~~~~~~~~~

.. code-block:: python

   def cfg_from_str(raw_cfg_text: str, allow_override: bool = False) -> None

指定された設定文字列から設定を構築します。

**Arguments**\ :


* ``raw_cfg_text`` *str* - コンフィグのファイルで使用されるのと同じ構文を使用して引数を宣言する文字列。
* ``allow_override`` *bool, optional* - 他のソース（例えば別の .ini 設定ファイルや設定文字列）から設定を上書きするフラグ。デフォルトは ``False``。

:raw-html-m2r:`<a id="Configer.Configer.cfg_from_ini"></a>`

cfg_from_ini
~~~~~~~~~~~~

.. code-block:: python

   def cfg_from_ini(cfg_path: str, allow_override: bool = False) -> None

指定された .ini コンフィグのファイルから設定を構築します。

**Arguments**\ :


* ``cfg_path`` *str* - .ini 設定ファイルが格納されているパス。
* ``allow_override`` *bool, optional* - 他のソース（例えば別の .ini 設定ファイルや設定文字列）から設定を上書きするフラグ。デフォルトは ``False``。

:raw-html-m2r:`<a id="Configer.Configer.args_from_cmd"></a>`

args_from_cmd
~~~~~~~~~~~~~

.. code-block:: python

   def args_from_cmd() -> None

コマンドライン入力文字列によって引数を更新します。
このメソッドは、予め定義された設定をネイティブに（サイレントモードで）上書きすることを許可します。
（コマンドライン入力は明示的にユーザーによって与えられるため、警告は不要です）

:raw-html-m2r:`<a id="Configer.Configer.__or__"></a>`

__or__
~~~~~~

.. code-block:: python

   def __or__(cfg)

2つの設定をマージし、左辺の設定を右辺の設定で上書きします。
例えば、``cfg_a = cfg_a | cfg_b`` の場合、``cfg_a`` は ``cfg_b`` によって上書きされます。

**Arguments**\ :


* ``cfg`` *AttributeDict* - 引数を格納するコンテナ。dict を継承しており、入力されたデータはネストされた辞書である可能性があります。

:raw-html-m2r:`<a id="Configer.Configer.__add__"></a>`

__add__
~~~~~~~

.. code-block:: python

   def __add__(cfg)

2つの設定をマージし、いずれの設定も上書きしません。
このメソッドは内部で ``self.concate_cfg(.)`` を呼び出します。

**Arguments**\ :


* 
  ``cfg`` *AttributeDict* - 引数を格納するコンテナ。dict を継承しており、入力されたデータはネストされた辞書である可能性があります。

  Raise:
  引数の再定義がある場合、``RuntimeError`` を発生させます。

:raw-html-m2r:`<a id="Configer.Configer.concate_cfg"></a>`

concate_cfg
~~~~~~~~~~~

.. code-block:: python

   def concate_cfg(cfg)

2つの設定をマージし、いずれの設定も **上書きしません**。

**Arguments**\ :


* 
  ``cfg`` *AttributeDict* - 引数を格納するコンテナ。dict を継承しており、入力されたデータはネストされた辞書である可能性があります。

  Raise:
  引数の再定義がある場合、``RuntimeError`` を発生させます。

**Returns**\ :

  Configer インスタント。

:raw-html-m2r:`<a id="Configer.Configer.merge_conf"></a>`

merge_conf
~~~~~~~~~~

.. code-block:: python

   def merge_conf(cfg, override=True)

2つの設定をマージし、右辺の設定で左辺の設定を上書きします。

**Arguments**\ :


* ``cfg`` *AttributeDict* - 引数を格納するコンテナ。dict を継承しており、入力されたデータはネストされた辞書である可能性があります。
* ``override`` *bool* - 設定を上書きするかどうかを示すフラグ。デフォルトは ``True``。

**Returns**\ :

  None. この操作はインプレース(inplace operation)で行われます。

:raw-html-m2r:`<a id="Configer.Configer.__str__"></a>`

__str__
~~~~~~~

.. code-block:: python

   def __str__()

設定で定義されたすべての'非プライベート'引数を表示する。

:raw-html-m2r:`<a id="Configer.Configer.__iter__"></a>`

__iter__
~~~~~~~~

.. code-block:: python

   def __iter__()

Configer のイテレータを返します。Configer 自体は辞書ではないため、このメソッドをサポートします。

:raw-html-m2r:`<a id="Configer.Configer.__getitem__"></a>`

__getitem__
~~~~~~~~~~~

.. code-block:: python

   def __getitem__(key)

Configer で ``getitem`` をサポートします。Configer 自体は辞書ではないため、このメソッドをサポートします。

:raw-html-m2r:`<a id="Configer.Configer.__setitem__"></a>`

__setitem__
~~~~~~~~~~~

.. code-block:: python

   def __setitem__(key, value)

Configer で ``setitem`` をサポートします。Configer 自体は辞書ではないため、このメソッドをサポートします。

:raw-html-m2r:`<a id="Configer.Configer.get"></a>`

get
~~~

.. code-block:: python

   def get(key, default_value=None)

Configer で ``get`` をサポートします。Configer 自体は辞書ではないため、このメソッドをサポートします。

:raw-html-m2r:`<a id="Configer.Configer.get_cfg_flag"></a>`

get_cfg_flag
~~~~~~~~~~~~

.. code-block:: python

   def get_cfg_flag()

設定を同期するための FLAG オブジェクトを返します。

:raw-html-m2r:`<a id="Configer.Configer.get_doc_str"></a>`

get_doc_str
~~~~~~~~~~~

.. code-block:: python

   def get_doc_str()

ヘルパー情報文字列を返します。

:raw-html-m2r:`<a id="Configer.Configer.regist_cnvtor"></a>`

regist_cnvtor
~~~~~~~~~~~~~

.. code-block:: python

   def regist_cnvtor(type_name: str = None, cnvt_func: callable = None)

ユーザーがカスタマイズしたクラスを宣言します。登録されたタイプ（クラス）は設定ファイル内で引数として宣言する際に使用できます。

**Arguments**\ :

* 
  ``type_name`` *str* - 設定ファイルで使用されるタイプ名。例えば、'dummy' として登録された場合、設定ファイル内で ``var = {'arg1':42}@dummy`` と宣言できます。

* 
  ``cnvt_func`` *callable* - 通常はカスタマイズしたクラスのコンストラクタです。カスタマイズしたクラスをそのまま引数として渡すことができます。

**Returns**\ :

  None この登録メソッドはフラグを返しません。

:raw-html-m2r:`<a id="Configer.Configer.split_char"></a>`

split_char
~~~~~~~~~~

.. code-block:: python

   @property
   def split_char()

設定ファイルで使用される区切り文字（split character）を表示します。
