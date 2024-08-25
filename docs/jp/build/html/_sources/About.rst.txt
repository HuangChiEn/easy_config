.. role:: raw-html-m2r(raw)
   :format: html


.. image:: assets/logo.png
   :target: assets/logo.png
   :alt: easy-configer logo


このプロジェクトについて
========================

序文 ✨
^^^^^^^^^

easy_configer バージョン : 2.3.2

..

   小提示 :  2.3.1 版只是對 pypi 上文檔的修正

気楽にプログラムを制御できます 

使用者にPythonプログラムの設定を行う軽量な構成ツールを提供することを光栄に思います。
このツールが大規模なプロジェクトを容易に制御できるように願っています。


開発の背景について 📝
^^^^^^^^^^^^^^^^^^^^^
大規模なプロジェクトでの複雑な業務ロジックを制御するために、多くのパラメータが必要とされます。
そして、このツールが使いやすくなることで、ユーザーがこれらのパラメータを簡単に制御できることが期待されています。
現在、多くのパッケージがこの機能を提供していますが、完全な解決策は見当たらないと述べています。
代わりに、これらのパッケージはそれぞれ長所と短所を持っており、短所がプログラムを冗長にし、読み込みにくくしています。

例えば、

.. code-block:: python

   ## ConfigParser
   import ConfigParser 
   Config = ConfigParser.ConfigParser()
   Config.read("c:\\tomorrow.ini")
   # get arg via method
   Config.get(section, option)
   # or get arg with converter
   int(Config['lucky_num'])

   ## Argparse
   import argparse
   parse = argparse.ArgumentParser("description string")
   parse.add_argument("--lucky_num", type=int)
   ...
   args = parser.parse_args()
   args.lucky_num



これを受けて、私はこれらの問題に対処する新しい解決策を提案します。
easy_configerには、以下の特長が含まれます：

#. 
   **階層的なコンフィグ　(多層次的字典結構)**

#. 
   **複数の設定ファイルを受け入れ、動的な読み込みをサポート**

#. 
   **カスタムデータ型のサポート（キーワードパラメータによってクラスを初期化します）**

#. 
   **コマンドラインで任意の設定値を更新できます。その値の階層に関係なく**

#. 
   **abslスタイルのフラグ機能をサポート** 

また、解決策は以下の機能もサポートしています：

* 
  どんなパラメータでもドット演算子を使用してアクセスできます（辞書内の辞書のパラメータでも）

* 
  行内での "#" を使用したコメントアウトが可能です

* 
  シングルラインでコンフィグのパラメータ補間をサポートします！！

* 
  easy_configを他の設定パッケージ（omegaconf、argparse、...などのサードパーティパッケージ）のコンフィグに変換することが可能です

* 
  ダイナミックに多層的なコンフィグをオーバーロードをシステムをサポートします ~　
