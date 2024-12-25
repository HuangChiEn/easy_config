.. role:: raw-html-m2r(raw)
   :format: html


常用参考情报
=============

1. 階層化配置の定義方法 🖋️
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Easy-configでは、2つのパラメータの準備方法があります：フラットパラメータを定義するか、複数のパラメータを階層化してグループ化することができます（2番目のレベルから）。
ほとんどの場合、フラットパラメータをグローバル設定として定義し、残りのパラメータを対応する辞書に配置して、サブプロシージャに割り当てやすくします。
ディープラーニングの例を挙げてみましょう。

*hier_cfg.ini あなたの作業ディレクトリに置いておきます*

.. code-block:: ini

   glb_seed = 42
   exp_id = '0001'

   # we call '...' in [...] as section name,
   # i.e. we can assign dict dataset to subroutine by `build_dataset(**cfg.dataset)`, just such easy!!
   [dataset]   
       service_port = 65536
       path = '/data/kitti'
       # of course, nested dict is also supported! it just the native python dictionary in dictionary!
       [dataset.loader]
           batch_size = 32

   [model]
       [model.backbone]
           mod_typ = 'resnet'
           [model.backbone.optimizer]
               lay_seed = 42  

   [train_cfg]
       batch_size = 32
       [train_cfg.opt]
           opt_typ = 'Adam'
           lr = 1e-4
           sched = 'cos_anneal'


構成ファイルが定義されています， ``python quick_hier.py`` を実行して、どのようにパラメータにアクセスするかを確認してみましょう。

.. code-block:: python

   from easy_configer.Configer import Configer

   if __name__ == "__main__":
       cfger = Configer(cmd_args=True)

       # omit cfg_from_str, hier-config also could be declared in str though ~
       cfger.cfg_from_ini("./hier_cfg.ini")

       print(cfger.dataset)  
       # output nested dict : { 'service_port':65536, 'path':'/data/kitti', 'loader':{'batch_size':32} }

       print(f"key-string access bz : {cfger.dataset['loader']['batch_size']}")
       # output - "key-string access bz : 32"

       print(f"bz : {cfger.dataset.loader.batch_size}")
       # output - "dot-access bz : 32"

       # we usually conduct initialization such simple & elegant!
       ds = build_dataset(**cfger.dataset)
       mod = build_model(**cfger.model)
       ... # get torch Trainer
       Trainer(mod).fit(ds)


構成ファイルの構文を改善することができますね。たとえば、 ``batch_size`` が ``dataset.loader`` と ``train_cfg`` の両方で2回定義されています。同様に、 ``layer_seed`` も同様です。
また、path がPython文字列として定義されており、さらにPython標準パッケージのPathオブジェクトに変換する必要があります。カスタムデータ型を登録することは可能ですか？
はい、これらの問題を優雅に解決することができます。パラメータの挿入を使用して最初の問題を解決し、2番目の問題を解決するためにカスタム登録を使用できます。

*記号$の設定挿入* とカスタム登録メソッド ``regist_cnvtor`` を使用して、問題を解決できます。

..

   現在、私たちは異なるネストされた辞書レベルの　**任意のパラメータ**　に対して挿入をサポートしています。さらに、bashの環境変数にアクセスするために　**$Env**　をサポートしています！


.. code-block:: python

   # For convience, we define string-config!
   def get_str_cfg():
       ''' # `export glb_seed=42` in bash!!
           glb_seed = ${env.glb_seed}@int   # or ${env.glb_seed} for short
           exp_id = '0001'

           [dataset]   
               service_port = 65536

               # Don't forgot to regist Path object first and the typename will be the given name!!
               path = {'path':'/data/kitti'}@pyPath

               [dataset.loader]
                   batch_size = 32
                   secrete_seed = 55688

           [model]
               [model.backbone]
                   mod_typ = 'resnet'
                   [model.backbone.optimizer]
                       # aweason! but we can do more crazy stuff ~
                        lay_seed = ${cfg.glb_seed}
                        # 'cfg' is used to access the config, feel free to access any arguments defined previsouly!!
                        string_seed = "The secrete string in data loader is ${cfg.dataset.loader.secrete_seed}!!"

           [train_cfg]
               batch_size = ${cfg.dataset.loader.batch_size}
               exp_id = "${cfg.exp_id}"  # or ${cfg.exp_id}@str, quote can not be omitted!
               [train_cfg.opt]
                   opt_typ = 'Adam'
                   lr = 1e-4
                   sched = 'cos_anneal'
       '''

   # main_block 
   if __name__ == "__main__":
       from pathlib import Path

       cfger = Configer(description="sample for arguments interpolation")
       cfger.regist_cnvtor("pyPath", Path)  # regist customer class 'Path'

       cfg_str = get_str_cfg()
       cfger.cfg_from_str(cfg_str)
       # do whatever you want to do!

----


2. 素早くすべての構成パラメータにアクセスできるようにします 🔓
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``easy_configer>=v2.4.0`` では、セクションの下で宣言された各引数は、``AttributeDict``と呼ばれる特別な辞書オブジェクトに格納されます（これはネイティブな Python の ``dict`` から継承しています）。これは、ネストされたオブジェクトにドット演算子でアクセスできる新しいコンテナです。 
``AttributeDict`` についての唯一の落とし穴は、その ``__dict__`` プロパティにアクセスしてはいけないことです。これは無効化されています。
簡単なブレーク‵`ポイントを設定して、 ``easy_configer.utils.Container.AttributeDict`` がパラメータのアクセスをどのぐらいにサポートしているかを体験してみましょう。

.. code-block:: python

   from easy_configer.Configer import Configer

   if __name__ == "__main__":
       cfger = Configer()
       cfger.cfg_from_ini("./hier_cfg.ini")
       breakpoint()

組態ファイルを作成しましょう、　``hier_cfg.ini``\ !!

.. code-block:: python

    # nested-dict
    [secA] # test depth ((sub^4)-section under secA)
        lev = 1
        [secA.secB]
            lev = 2
            [secA.secB.secC]
                lev = 3
                [secA.secB.secC.secD]
                    lev = 4


各階層の ``lev`` 変数にアクセスできるようにします :

#. ``(pdb) cfger.secA.lev``\ , 出力 ``lev : 1``
#. ``(pdb) cfger['secA'].secB['lev']``\ , 出力 ``lev : 2``\ , 続く..
#. 最もクレイジーな例を示します ~ ``(pdb) cfger.secA.['secB'].secC['secD'].lev``\ , 出力 ``lev : 4``

----

3. コマンドラインのサポート ⌨️
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..

   同様に ``hier_cfg.ini`` を例として!


.. code-block:: ini

   # hier_cfg.ini
   glb_var = 42@int
   [dataset]         
       ds_type = None
       path = {'root':'/data/kitti'}@Path
       [dataset.loader]
           batch_size = 32@int

   # Hier-Cell cfg written by Josef-Huang..


Python　で実行してヘルプ情報を出力します :raw-html-m2r:`<br>`
``python quick_hier.py -h``

非階層なパラメータを更新して、ヘルプ情報を出力します :raw-html-m2r:`<br>`
``python quick_hier.py glb_var=404 -h``

特に、 **階層なパラメータ**\，について、
コマンドラインで任意のレベルのパラメータにアクセスし、パラメータを更新できます。現在、任意のネストされたパラメータを変更してみてください。:raw-html-m2r:`<br>`
``python quick_hier.py dataset.ds_type="'kitti'" dataset.path="{'path':'/root/ds'}" dataset.loader.batch_size=48``

( 文字列の宣言は少し複雑ですが、現時点では2つの方法のみをサポートしています： 
    ``dataset.ds_type="'kitti'"`` あるいは ``dataset.ds_type=kitti@str``\ 、一つ選んでください ~ )

----

4. サブコンフィグをロードします 🎎
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``omegaconf``\　のように、多くのユーザーは、構成ファイルを型に基づいて分割し、実行時に動的にマージすることを期待しています。
これは合理的な要求ですが、以前のバージョンのeasy-configでは、構成ファイルを型に基づいて分割し、実行時に動的に結合することができましたが、これには制限がありました： 

#. ``cfg_from_ini`` を2回呼び出すことができましたが。例えば、 ``cfg.cfg_from_ini('./base_cfg') ; cfg.cfg_from_ini('./override_cfg')``。しかし、これは設定が明確にロードされていないため、可読性が良くないです。
#. 設定のマージを使用することもできましたが。例えば、 ``new_cfg = base_cfg | override_cfg``。しかし、数多くの設定をマージする場合には優雅な解決策ではありませんでした。

現在、新しい方法　**sub-config**　を提供します。サブ構成を導入するために、行の先頭に簡単に　``>``　記号を置くことができるようになりました。
また、サブコンフィグでは、デフォルトでは宣言された引数をオーバーライドすることはできません。これは、引数を動的にオーバーライドするとコンフィグの追跡が困難になるためです。

..

   設定をオーバーライドしたい場合は、フラグ ``allow_override`` を ``True`` に設定してください。例えば、``cfg.cfg_from_ini(..., allow_override=True)`` や ``cfg.cfg_from_str(..., allow_override=True)`` のように指定します。
   サブコンフィグは、フラグの設定に従って設定をオーバーライドするか、``RuntimeError`` を発生させます。

.. code-block:: ini

   # ./base_cfg.ini
   glb_seed = 42@int
   [dataset]         
       > ./config/ds_config.ini

   [model]
       > ./root/config/model_config.ini

   # ./config/ds_config.ini
   ds_type = None
   path = {'root':'/data/kitti'}@Path
   [dataset.loader]
       batch_size = 32@int

   # ./root/config/model_config.ini
   [model.backbone]
       mod_typ = 'resnet'
       [model.backbone.optimizer]
       # and yes, interpolation is still valid "after" the reference argument is declared!
           lay_seed = ${cfg.glb_seed}

----

5. コンフィグ運算子 ⛩️
~~~~~~~~~~~~~~~~~~~~~~~~~~

コンフィグ運算子は、動的構成システムの中核的な技術の1つです。
以下の例では、マージ構成システムが印象的な階層的なマージ機能を提供していることが示されています。

..

   例えば、cfg_a cfg_aの変数はcfg_bで置き換えることができます。ただし、それらは同じセクションブロック内に配置され、
   同じ名前の変数　``ghyu.opop.add``　を持つ必要があります。異なる名前空間は、それらの変数の値を安全に保持します。
   その故に、　``ghyu.opop.add``　の値は67になり、　``ghyu.opop.tueo.inpo``　の値はフラットパラメータinpoを参照して46になります。


.. code-block:: python

   from easy_configer.Configer import Configer

   def build_cfg_text_a():
       return '''
       # Initial config file :
       inpo = 46@int
       [test]         
           mrg_var_tst = [1, 3, 5]@list
           [test.ggap]
               gtgt = haha@str

       [ghyu]
           [ghyu.opop]
               add = 32@int
               [ghyu.opop.tueo]
                   salt = ${cfg.inpo}

       # Cell cfg written by Josef-Huang..
       '''

   def build_cfg_text_b():
       return '''
       # Initial config file :
       inop = 32@int
       [test]         
           mrg_var_tst = [1, 3, 5]@list
           [test.ggap]
               gtgt = overrides@str
               [test.ggap.conf]
                   secert = 42@int

       [ghyu]
           [ghyu.opop]
               add = 67@int
               div = 1e-4@float

       [new]
           [new.new]
               newsec = wpeo@str
       # Cell cfg written by Josef-Huang..
       '''

   if __name__ == "__main__":
       cfg_a = Configer(cmd_args=True)
       cfg_a.cfg_from_str(build_cfg_text_a())  


       cfg_b = Configer()
       cfg_b.cfg_from_str(build_cfg_text_b())

       # default, override falg is turn off ~
       cfg_a.merge_conf(cfg_b, override=True)

       # `cfg_b = cfg_b | cfg_a`, operator support, warn to decrease the read-ability...
       # cfg_a will override the argument of cfg_b which share the identitical variable name in cfg_b!
       # operator support : `cfg_b |= cfg_a` == `cfg_b = cfg_b | cfg_a`


----

**その他の機能**

6. IO変換機能 🐙
~~~~~~~~~~~~~~~~~~~~~~~
``easy_configer`` 型の設定を他の設定インスタンスに変換するには、IO コンバータを提供しています。IO コンバータは、いくつかのよく知られた設定タイプをサポートしています。
以下の例のように、適切な引数を指定してメソッドを呼び出すだけで簡単に利用できます。

.. code-block:: python

   from dataclasses import dataclass
   from typing import Optional

   @dataclass
   class TableConfig:
       rows: int = 1

   @dataclass
   class DatabaseConfig:
       table_cfg: TableConfig = TableConfig()

   @dataclass
   class ModelConfig:
       data_source: Optional[TableConfig] = None

   @dataclass
   class ServerConfig:
       db: DatabaseConfig = DatabaseConfig()
       model: ModelConfig = ModelConfig()

   if __name__ == '__main__':
       from easy_configer.IO_Converter import IO_Converter

       # first import the IO_converter
       from easy_config.IO_Converter import IO_Converter
       cnvt = IO_Converter()

       # convert easy_config instance into the argparse instance
       argp_cfg = cnvt.cnvt_cfg_to(cfger, 'argparse')

       uargp_cfg = cnvt.cnvt_cfg_to(cfger, 'argparse', parse_arg=False)
       argp_cfg = uargp_cfg.parse_args()

       ## convert config INTO..
       # convert easy_config instance into the omegaconf instance
       ome_cfg = cnvt.cnvt_cfg_to(cfger, 'omegaconf')

       # convert easy_config instance into the "yaml string"
       yaml_cfg = cnvt.cnvt_cfg_to(cfger, 'yaml')

       # convert easy_config instance into the "dict"
       yaml_cfg = cnvt.cnvt_cfg_to(cfger, 'dict')

       ## convert into easy-config FROM..
       # argparse, omegaconf, yaml, dict ... is supported
       ez_cfg = cnvt.cnvt_cfg_from(argp_cfg, 'omegaconf')

       # Especially, it support "dataclass"!
       ds_cfg = ServerConfig()
       ez_cfg = cnvt.cnvt_cfg_from(ds_cfg, 'dataclass')



7. Abslスタイルのフラグパラメータ 🏳️
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..

   同じ構成ファイルに再宣言することなく、異なるPythonファイルで同じ構成ファイルにアクセスできる機能があります。
   同じ作業ディレクトリに utils.py というファイルを作成しました。
   
``main.py``\ を実行したとします :

.. code-block:: python

    from easy_configer.Configer import Configer
    from utils import get_var_from_flag

    if __name__ == "__main__":
       cfg = Configer()
       cfg.cfg_from_str("var = 32")

       # both should output 32 ~
       print(f"var from main : {cfg.var}")
       print(f"var from flag : { get_var_from_flag() }")


``get_var_from_flag`` 関数が別のファイルにある場合、その関数に入るとします。

.. code-block:: python

   from easy_configer.Configer import Configer

   def get_n_blk_from_flag():
       new_cfger = Configer()
       flag = new_cfger.get_cfg_flag()
       # test to get the pre-defined 'var'
       return flag.var

