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

このヘルパークラスは、設定文字列を対応する型の値にパースすることを目的としています。
セキュリティ上の問題に配慮して、``eval()`` を使って危険なコードをパースすることを防止しています。その代わりに、ast.literal_eval()を使用してパース機能を制限しており、デフォルトの型変換ツールを自由に使用できます。

:raw-html-m2r:`<a id="utils.Type_Convertor.Type_Convertor.__init__"></a>`

__init__
~~~~~~~~

.. code-block:: python

   def __init__(typ_split_chr: str = '@', filter_split_chr: str = ' | ')

type convertor のコンストラクタ。

**Arguments**\ :


* 
  ``typ_split_chr`` *str, option* - 設定ファイル内で宣言文字列を分割するために使用される文字。例えば、``a = 13@int`` のように、'a' は整数型データであり、``@`` は ``typ_split_chr`` です。デフォルト値は ``@``。

* 
  ``filter_split_chr`` *str, option* - 値文字列を分割して、解析された値に対する「後処理」を指定するための文字。例えば、``a = hello@str | upper`` のように、upper は後処理として 'a' を大文字に変換します。デフォルト値は ``|``。


:raw-html-m2r:`<a id="utils.Type_Convertor.Type_Convertor.convert"></a>`

convert
~~~~~~~

.. code-block:: python

   def convert(cfg_raw_str: str, tmp_cfg_node=None)

**Arguments**\ :

* 
  ``cfg_raw_str`` *str* - 設定ファイルで使用されるのと同じ構文で引数を宣言する文字列。

* 
  ``tmp_cfg_node`` *AttributeDict* - 引数を補完するために使用されるコンテナ。設定に定義されたすべての引数が格納されます。デフォルトは ``None``。

:raw-html-m2r:`<a id="utils.Type_Convertor.Type_Convertor.regist_cnvtor"></a>`

regist_cnvtor
~~~~~~~~~~~~~

.. code-block:: python

   def regist_cnvtor(type_name: str = None, cnvt_func: callable = None)

カスタマイズしたクラスの登録を行います。

**Arguments**\ :


* 
  ``type_name`` *str* - 登録する関数の名前、すなわちカスタマイズしたクラスの名前。デフォルトは ``None``。

* 
  ``cnvt_func`` *callable* - 文字列オブジェクトをカスタムクラスのインスタンスに変換するための関数。デフォルトは ``None``。

:raw-html-m2r:`<a id="utils.Type_Convertor.Type_Convertor.regist_filter"></a>`

regist_filter
~~~~~~~~~~~~~

.. code-block:: python

   def regist_filter(filter_name: str = None, filter_func: callable = None)

後処理関数を登録します。

**Arguments**\ :


* 
  ``type_name`` *str* - 登録する関数の名前。デフォルトは ``None``。

* 
  ``cnvt_func`` *callable* - 文字列オブジェクトをカスタムクラスのインスタンスに変換するための後処理関数。デフォルトは ``None``。
