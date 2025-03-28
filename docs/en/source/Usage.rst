.. role:: raw-html-m2r(raw)
   :format: html


Common Usage
================

1. How to declare hierachical config 🖋️
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There have two kind of way to prepare the arguments in easy-config : we can either define flatten argument or groupping the multiple arguments in an hierachical manner (begin from second level). In most of time, we define the flatten argument as global setup, and arrange the rest of arguments into the corresponding dictionary for easy to assign it to the subroutine.  
Let's give a deep-learning example ~

*hier_cfg.ini in work directory*

.. code-block:: ini

   root_dir = '/workspace'
   glb_seed = 42
   exp_id = '0001'

   # we call '...' in [...] as section name,
   # i.e. we can assign dict dataset to subroutine by `build_dataset(**cfg.dataset)`, just such easy!!
   [dataset]   
       service_port = 65536
       path = "${cfg.root_dir}/data/kitti"
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


We have defined the config file, now let's see how to access any agruments! Execute ``python quick_hier.py`` in work directory.

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


However, the syntax in config could be improved, isn't it !? For example, the batch_size is defined twice under ``dataset.loader`` and ``train_cfg``, so as layer seed.
Moreover, path is defined as python string, it need to be further converted by Path object in python standard package. Could we regist our customized data type for easy-config ?
Glade to say : Yes! it's possible to elegantly deal with above mentioned issue. We can solve the first issue by using argument interpolation, and solve the second issue by using the customized register!!

Python **フォーマット文字列** ``${...}`` と **カスタマイズされた登録メソッド** ``regist_cnvtor`` に感謝します。 下記の例を参照してください :

..

   Currently we support interpolation mechnaism to interpolate **ANY** arguemnts even beloning to nested section by simply using **\${cfg}** notation. Moreover, we also support **\${env}** for accessing enviroment variables exported in bash!!


.. code-block:: python

   # For convience, we define string-config!
   def get_str_cfg():
       ''' # `export glb_seed=42` in bash!!
           glb_seed = ${env.glb_seed}@int   # or ${env.glb_seed} for short
           exp_id = '0001'

           [dataset]   
               service_port = 65536

               # Don't forgot to regist Path object first and the typename will be the given name!!
               path = ['/data/kitti']@pyPath

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


2. Access all arguments flexibly 🔓
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
For ``easy_configer>=v2.4.0``, each argument declared under section will be stored in a special dictionary object, called ``AttributeDict`` (Inhert from native python ``dict``). It's a new container allowing dot-operator for accessing any nested object.
The only pitfall about ``AttributeDict`` is that **you should never access its ``__dict__`` property**, since it's disabled..
We simple set a breakpoint to feel how flexible does ``easy_configer.utils.Container.AttributeDict`` support.

.. code-block:: python

   from easy_configer.Configer import Configer

   if __name__ == "__main__":
       cfger = Configer()
       cfger.cfg_from_ini("./hier_cfg.ini")
       breakpoint()

We write a special example ``hier_cfg.ini``\ !!

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


Now you can access each ``lev`` :

#. ``(pdb) cfger.secA.lev``\ , output ``lev : 1``
#. ``(pdb) cfger['secA'].secB['lev']``\ , output ``lev : 2``\ , and so on..
#. Most crazy one ~ ``(pdb) cfger.secA.['secB'].secC['secD'].lev``\ , output ``lev : 4``

----

3. Commmend-line Support ⌨️
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..

   We also take ``hier_cfg.ini`` as example!


.. code-block:: ini

   # hier_cfg.ini
   glb_var = 42@int
   [dataset]         
       ds_type = None
       path = ['/data/kitti']@pyPath
       [dataset.loader]
           batch_size = 32@int


Execute python program and print out the helper information :raw-html-m2r:`<br>`
``python quick_hier.py -h``

Update flatten argument and print out the helper information :raw-html-m2r:`<br>`
``python quick_hier.py glb_var=404 -h``

Especially update **non-flatten argument**\ , you can access any argument at any level by dot-access in commend-line!! (with combining any argument update). Now, try to change any nested argument :raw-html-m2r:`<br>`
``python quick_hier.py dataset.ds_type="'kitti'" dataset.path=['/root/ds'] dataset.loader.batch_size=48``

( Note that the commendline declaration for string is tricky, but currently we only support two way for that : 
    ``dataset.ds_type="'kitti'"`` or ``dataset.ds_type=kitti@str``\ , pick up one of you like ~ )

----

4. Import Sub-Config 🎎
~~~~~~~~~~~~~~~~~~~~~~~~~~

Like ``omegaconf``\ , most of user expect to seperate the config based on their category and dynamically merge it in runtime. It's a rational requirement and the previous version of easy-config provide two way to conduct it, but both have it's limit : 


#. you can call the ``cfg_from_ini`` twice, for example, ``cfg.cfg_from_ini('./base_cfg', allow_overwrite=True) ; cfg.cfg_from_ini('./override_cfg', allow_overwrite=True)``. But it's not explicitly load the config thus reducing readability.
#. you can use the config merging, for example, ``new_cfg = base_cfg | override_cfg``. But it's not elegant solution while you  have to merge several config..

Now, we provide the thrid way : **sub-config**. you can import the sub-config in any depth of hierachical config by simply placing the ``>`` symbol at the beginning of line.
Also note that sub-config doesn't allow you override the declared **section** by default, since dynamically override the section is not necessary generally (also made your config hard to trace).

.. code-block:: ini

   # ./base_cfg.ini
   glb_seed = 42@int
   [dataset]         
       > ./config/ds_config.ini

   [model]
       > ./root/config/model_config.ini

   # ./config/ds_config.ini
   ds_type = None
   path = ['/data/kitti']@pyPath
   [dataset.loader]
       batch_size = 32@int

   # ./root/config/model_config.ini
   [model.backbone]
       mod_typ = 'resnet'
       [model.backbone.optimizer]
       # and yes, interpolation is still valid "after" the reference argument is declared!
           lay_seed = ${cfg.glb_seed}

Also note that we still recommend you create several config instance and merge it in 2. way, if you want to merge it with overwriting manner. Instead of acting like omegaconf, it dynamically overwrite your config silently..

..

    If you **still** want to overwrite the config (act like omegaconf), turn the flag allow_overwrite as True. i.e. ``cfg.cfg_from_ini(..., allow_overwrite=True)``, ``cfg.cfg_from_str(..., allow_overwrite=True)``. The sub-config will follow the flag setting to overwrite the config. Be careful of the order, the **imported sub-configs** are considered as **'default setup'**, the main config (which import sub-configs) setup will overwrite its.  

.. code-block:: ini
        
    # ./base_cfg.ini

    # note that the order between defined arguments and imported sub-config do affect the final value of arguments!
    glb_seed = 42

    # import several default setup :
    > ./config/ds_config.ini
    > ./config/model_config.ini

    [dataset]       
        n_worker = 8

    [model]
        n_blk = 2

    # ./config/ds_config.ini
    [dataset]
        n_worker = 1
        path = ['/data/kitti']@pyPath
        [dataset.loader]
            batch_size = 32@int

    # ./root/config/model_config.ini
    [model]
        mod_typ = 'resnet'
        n_blk = 1
        [model.optimizer]
        # and yes, interpolation is still valid "after" the reference argument is declared!
            lay_seed = ${cfg.glb_seed}

After dynamic loading :

.. code-block:: ini

    glb_seed = 42

    [dataset]       
        n_worker = 8  # overwrited by base_cfg.ini
        path = ['/data/kitti']@pyPath
        [dataset.loader]
            batch_size = 32@int

    [model]
        n_blk = 2 # overwrited by base_cfg.ini
        mod_typ = 'resnet'
        [model.optimizer]
            lay_seed = 42
            
----

5. Config Operation ⛩️
~~~~~~~~~~~~~~~~~~~~~~~~~

Config operation is one of the core technique for dynamic configuration system!!
In the following example, you can see that the merging config system already provided a impressive hierachical merging funtionality! 

..

   For example, ``ghyu.opop.add`` in cfg_a can be replaced by the cfg_b in **same** section with the same variable name, while the different namespace keep their variable safely ~ so the value of ``ghyu.opop.add`` will be 67 and ``ghyu.opop.tueo.inpo`` refer the flatten variable ``inpo`` and the value will be 46.


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

**Miscellnous features**

6. IO Converter 🐙
~~~~~~~~~~~~~~~~~~~~~~~
To convert the `easy_configer` type config into the other config instance, we provide a IO converter to serve for this requirement. IO converter support several well-know config type.. Just simple call the method with the proper arguments as the following example. 

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



7. Absl style flag 🏳️
~~~~~~~~~~~~~~~~~~~~~~~~~~

..

   easy_config also support that you can access the 'same' config file in different python file without re-declare the config. utils.py under the same work directory

Suppose you have executed ``main.py``\ :

.. code-block:: python

    from easy_configer.Configer import Configer
    from utils import get_var_from_flag

    if __name__ == "__main__":
       cfg = Configer()
       cfg.cfg_from_str("var = 32")

       # both should output 32 ~
       print(f"var from main : {cfg.var}")
       print(f"var from flag : { get_var_from_flag() }")

Now, when you step in ``get_var_from_flag`` function in different file..
    
.. code-block:: python

   from easy_configer.Configer import Configer

   def get_n_blk_from_flag():
       new_cfger = Configer()
       flag = new_cfger.get_cfg_flag()
       # test to get the pre-defined 'var'
       return flag.var

