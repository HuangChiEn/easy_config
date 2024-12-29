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

easy_config インスタンスを他の一般的な設定インスタンスに変換するインターフェース、およびその逆を行うインターフェースです。
注意：変換結果はターゲット設定のサポートに応じて若干異なる場合があります。例えば、argparse は階層的な設定を明示的に格納する方法を提供していないため、変換された設定はフラット化されます。

:raw-html-m2r:`<a id="IO_Converter.IO_Converter.__init__"></a>`

__init__
~~~~~~~~

.. code-block:: python

   def __init__()

コンバータのコンストラクタ。ここで、easy_config インスタンスを指定されたサブルーチンにディスパッチするための入力/出力ディスパッチャを宣言します。

:raw-html-m2r:`<a id="IO_Converter.IO_Converter.cnvt_cfg_to"></a>`

cnvt_cfg_to
~~~~~~~~~~~

.. code-block:: python

   def cnvt_cfg_to(cfg, target_cfg_type: str, **cnvtr_kwarg)

easy_configer を他の一般的な設定インスタンスに変換します。

**Arguments**\ :


* ``cfg`` *Configer* - easy_configer インスタンス。
* ``target_cfg_type`` *str* - サポートされている設定タイプの文字列タグ。``self.output_dispatcher.keys()`` で確認できます。
* ``cnvtr_kwarg`` *kwargs* - その他のキーワード引数、変換サブルーチンに渡すためのものです。

**Returns**\ :
   Any, ターゲット設定インスタンス。

:raw-html-m2r:`<a id="IO_Converter.IO_Converter.cnvt_cfg_from"></a>`

cnvt_cfg_from
~~~~~~~~~~~~~

.. code-block:: python

   def cnvt_cfg_from(other_cfg, target_cfg_type: str, **cnvtr_kwarg)

指定された一般的な設定インスタンスから easy_configer に変換します。

**Arguments**\ :


* ``other_cfg`` *Any* - 任意のサポートされた設定インスタンス。
* ``target_cfg_type`` *str* - サポートされている設定タイプの文字列タグ。``self.input_dispatcher.keys()`` で確認できます。
* ``cnvtr_kwarg`` *kwargs* - その他のキーワード引数、変換サブルーチンに渡すためのものです。

**Returns**\ :
  Configer インスタンス。
