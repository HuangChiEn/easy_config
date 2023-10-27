.. role:: raw-html-m2r(raw)
   :format: html


常用參考資訊
=============

1. 如何定義階層化配置 🖋️
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在 easy-config 中，有兩種準備參數的方式：我們可以定義扁平參數，也可以將多個參數以層次化的方式進行分組（從第二層級開始）。
在大多數情況下，我們將扁平參數定義為全局設置，並將其餘的參數安排到相應的字典中，以便於將其分配給子程序。
讓我們舉一個深度學習的例子~

*hier_cfg.ini 放置於您的工作目錄中*

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


我們已經定義了配置文件，現在讓我們看看如何訪問任何參數！在工作目錄中執行 ``python quick_hier.py``。

.. code-block:: python

   from easy_configer.Configer import Configer

   if __name__ == "__main__":
       cfger = Configer(cmd_args=True)

       # omit cfg_from_str, hier-config also could be declared in str though ~
       cfger.cfg_from_ini("./hier_cfg.ini")

       print(cfger.dataset)  
       # output nested dict : { 'service_port':65536, 'path':'/data/kitti', 'loader':{'batch_size':32} }

       print(cfger.dataset['loader']['batch_size'])
       # output : 32

       # we usually conduct initialization such simple & elegant!
       ds = build_dataset(**cfger.dataset)
       mod = build_model(**cfger.model)
       ... # get torch Trainer
       Trainer(mod).fit(ds)


然而，上面的配置文件的語法可以進行改進, 對吧! 例如 : ``batch_size`` 在 ``dataset.loader`` 和 ``train_cfg`` 下都被定義了兩次；同樣地, ``layer_seed`` 也是如此。
此外，path 被定義為 Python 字符串，需要進一步通過 Python 標準包中的 Path 對象進行轉換。我們能夠註冊我們自定義的數據類型嗎？
很高興地告訴您：是的！可以優雅地處理上述問題。我們可以通過使用參數插值來解決第一個問題，通過使用自定義註冊來解決第二個問題！

使用 *$ 符號的配置插值* 以及 自定義的註冊方法 ``regist_cnvtor``。

..

   Currently we support interpolation mechnaism to interpolate **ANY** arguemnts belong the different level of nested dictionary. Moreover, we also support **$Env** for accessing enviroment variables exported in bash!!


.. code-block:: python

   # For convience, we define string-config!
   def get_str_cfg():
       ''' # `export glb_seed=42` in bash!!
           glb_seed = $Env.glb_seed
           exp_id = '0001'

           [dataset]   
               service_port = 65536

               # Don't forgot to regist Path object first and the typename will be the given name!!
               path = {'path':'/data/kitti'}@pyPath

               [dataset.loader]
                   batch_size = 32

           [model]
               [model.backbone]
                   mod_typ = 'resnet'
                   [model.backbone.optimizer]
                       lay_seed = $glb_seed

           [train_cfg]
               batch_size = $dataset.loader.batch_size
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

2. 命令列支援 ⌨️
~~~~~~~~~~~~~~~~~

..

   我們同樣用 ``hier_cfg.ini`` 作為範例!


.. code-block:: ini

   # hier_cfg.ini
   glb_var = 42@int
   [dataset]         
       ds_type = None
       path = {'root':'/data/kitti'}@Path
       [dataset.loader]
           batch_size = 32@int

   # Hier-Cell cfg written by Josef-Huang..


執行 Python 程序並打印出幫助信息 :raw-html-m2r:`<br>`
``python quick_hier.py -h``

更新扁平參數並打印出幫助信息 :raw-html-m2r:`<br>`
``python quick_hier.py glb_var=404 -h``

特別是更新 **非扁平參數**\，您可以在命令行中通過點擊訪問任何層級的參數！（結合任何參數更新）。現在，試著更改任何嵌套的參數。:raw-html-m2r:`<br>`
``python quick_hier.py dataset.ds_type="'kitti'" dataset.path="{'path':'/root/ds'}" dataset.loader.batch_size=48``

( 請注意，命令行中字符串的聲明有點棘手，但目前我們只支援兩種方式： 
    ``dataset.ds_type="'kitti'"`` 或 ``dataset.ds_type=kitti@str``\ , 選一個你喜歡的 ~ )

----

3. 載入子配置 🎎
~~~~~~~~~~~~~~~~~

如同 ``omegaconf``\ , 大多數用戶期望根據類型將配置文件分開並在運行時動態合併它們。這是一個合理的需求，之前版本的 easy-config 提供了兩種進行此操作的方式，但都有其限制： 

#. 您可以呼叫 ``cfg_from_ini`` 兩次, 例如, ``cfg.cfg_from_ini('./base_cfg') ; cfg.cfg_from_ini('./override_cfg')``。但這樣做並未明確載入配置，從而降低了可讀性。
#. 您可以使用配置合併，例如 : ``new_cfg = base_cfg | override_cfg``。但是當您需要合併多個配置時，這並不是一個優雅的解決方案...

現在，我們提供了第三種方式 : **sub-config**。您可以通過在行首簡單地放置 ``>`` 符號來在層次配置的任何階層導入子配置。

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
           lay_seed = $glb_seed  

----

4. 配置運算子 ⛩️
~~~~~~~~~~~~~~~~~~

配置運算子是動態配置系統的核心技術之一!!
在下面的例子中，您可以看到合併配置系統已經提供了令人印象深刻的層次合併功能!

..

   例如, cfg_a 中的變量可以被 cfg_b 替換，只要他們置於相同 section 區塊中，並為同名變量 ``ghyu.opop.add``；而不同的命名空間會保持它們的變量值安全。
   因此， ``ghyu.opop.add`` 的值將變為 67，而 ``ghyu.opop.tueo.inpo`` 的值將參照扁平參數 ``inpo``，並變成 46。


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
                   salt = $inpo

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

**其餘功能**

5. IO 轉換器 🐙
~~~~~~~~~~~~~~~~~~~~~~~

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
       db: DatabaseConfig
       model: ModelConfig

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



6. Absl 風格的旗標參數 🏳️
~~~~~~~~~~~~~~~~~~~~~~~~~~

..

   easy_config 也支持您可以在不同的 Python 文件中訪問"相同"的配置文件，而無需重新聲明配置。在相同的工作目錄下創建一個名為 test_flag.py 的文件。


.. code-block:: python

   from easy_configer.Configer import Configer

   def get_n_blk_from_flag():
       new_cfger = Configer()
       flag = new_cfger.get_cfg_flag()
       # test to get the pre-defined 'n_blk'
       return flag.n_blk

