.. role:: raw-html-m2r(raw)
   :format: html


.. image:: assets/logo.png
   :target: assets/logo.png
   :alt: easy-configer logo


このプロジェクトについて
========================

序文 ✨
^^^^^^^^^

easy_configer バージョン : 2.5.6

..

   ドキュメントは工事中です、英語のドキュメント参照してください。

気楽にプログラムを制御できます 

使用者にPythonプログラムの設定を行う軽量な構成ツールを提供することを光栄に思います。
このツールが大規模なプロジェクトを容易に制御できるように願っています。


開発の背景について 📝
^^^^^^^^^^^^^^^^^^^^^

🙋‍♂️ なぜ easy_configer ?
"""""""""""""""""""""""""""""""""

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

   ## Omegaconf
   from omegaconf import OmegaConf
   conf = OmegaConf.load('source/example.yaml')
   conf.player.height

omegaconf　以外のほとんどの設定ツールは、設定引数を読み込んでアクセスするために冗長な構文が多くあります。
しかし、「omegaconf」にはいくつかの欠点もあります：

#. 
   依存関係が多すぎる（バージョンの互換性が問題になる可能性がある！）

#. 
   動的な設定読み込みシステムが追跡しづらい（どの設定が私のデフォルト設定を上書きしたのかが分かりづらい）

#. 
   ネイティブではないコンテナ（Mappableオブジェクトが適用されるため、さらに変換するにはto_containerを適用する必要がある）

これを受けて、私はこれらの問題に対処する新しい解決策を提案します。
easy_configerには、以下の特長が含まれます：

#. 
   ゼロ依存関係！！（他の設定ツールインスタンスに変換したい場合を除く）

#. 
   柔軟な適用 :code:`allow_overwrite=False` を設定すれば、上書きされた引数を簡単に検出できます。

#. 
   当社のコンテナは純粋なPythonの辞書を継承！ほとんどの辞書メソッドもそのまま使用可能です。

私のソリューションは、以下の属性にも対応しています：

#. 
   **階層的なコンフィグ　(多層次的字典結構)**

#. 
   **複数の設定ファイルを受け入れ、動的な読み込みをサポート (omegaconfみたいです)**

#. 
   **カスタムデータ型のサポート（キーワード、リスト パラメータによってクラスを初期化します）**

#. 
   **コマンドラインで任意の設定値を作って更新できます。その値の階層に関係なく**

#. 
   **abslスタイルのフラグ機能をサポート (一度定義して、どこでも使えます)** 

また、解決策は以下の機能もサポートしています：

* 
  どんなパラメータでもドット演算子を使用してアクセスできます（辞書内の辞書のパラメータでも）

* 
  行内での "#" を使用したコメントアウトが可能です

* 
  シングルラインでコンフィグのパラメータ補間をサポートします！！

* 
  easy_configを他の設定パッケージのコンフィグに変換することが可能です (omegaconf、argparse、...などのサードパーティパッケージ)

* 
  ダイナミックに多層的なコンフィグをオーバーロードをシステムをサポートします ~　
