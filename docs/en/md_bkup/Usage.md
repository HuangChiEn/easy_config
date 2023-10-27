
### Common usage
#### **1. How to declare hierachical config**
There have two kind of way to prepare the arguments in easy-config : we can either define flatten argument or groupping the multiple arguments in an hierachical manner (begin from second level). In most of time, we define the flatten argument as global setup, and arrange the rest of arguments into the corresponding dictionary for easy to assign it to the subroutine.  

#### Let's give a deep-learning example ~
#### *hier_cfg.ini in work directory*

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

#### We have defined the config file, now let's see how to access any agruments! Execute `python quick_hier.py` in work directory*.

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

However, the syntax of above config file could be improved, isn't it !? For example, the batch_size is defined twice under `dataset.loader` and `train_cfg`, so as layer seed. Moreover, path is defined as python string, it need to be further converted by Path object in python standard package. Could we regist our customized data type for easy-config ?
#### Glade to say : Yes! it's possible to elegantly deal with above mentioned issue. We can solve the first issue by using argument interpolation, and solve the second issue by using the customized register!!

#### *config interpolation with $ symbol* and  *customized register method `regist_cnvtor`*
> Currently we support interpolation mechnaism to interpolate **ANY** arguemnts belong the different level of nested dictionary. Moreover, we also support **$Env** for accessing enviroment variables exported in bash!!

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
        

#### **3. Commmend-line Support**
> We also take `hier_cfg.ini` as example!

    # hier_cfg.ini
    glb_var = 42@int
    [dataset]         
        ds_type = None
        path = {'root':'/data/kitti'}@Path
        [dataset.loader]
            batch_size = 32@int

    # Hier-Cell cfg written by Josef-Huang..

Execute python program and print out the helper information <br>
`python quick_hier.py -h`

Update flatten argument and print out the helper information <br>
`python quick_hier.py glb_var=404 -h`

Especially update **non-flatten argument**, you can access any argument at any level by dot-access in commend-line!! (with combining any argument update). Now, try to change any nested argument <br>
`python quick_hier.py dataset.ds_type="'kitti'" dataset.path="{'path':'/root/ds'}" dataset.loader.batch_size=48`

( Note that the commendline declaration for string is tricky, but currently we only support two way for that : 
    `dataset.ds_type="'kitti'"` or `dataset.ds_type=kitti@str`, pick up one of you like ~ )

#### **4. Import Sub-Config**
Like `omegaconf`, most of user expect to seperate the config based on their type and dynamically merge it in runtime. It's a rational requirement and the previous version of easy-config provide two way to conduct it, but both have it's limit : 
1. you can call the `cfg_from_ini` twice, for example, `cfg.cfg_from_ini('./base_cfg') ; cfg.cfg_from_ini('./override_cfg')`. But it's not explicitly load the config thus reducing readability.
2. you can use the config merging, for example, `new_cfg = base_cfg | override_cfg`. But it's not elegant solution while you  have to merge several config..

#### Now, we provide the thrid way : **sub-config**. you can import the sub-config in any depth of hierachical config by simply placing the `>` symbol at the beginning of line.
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


#### **5. Config Operation**
Config operation is one of the core technique for dynamic configuration system!!
In the following example, you can see that the merging config system already provided a impressive hierachical merging funtionality! 

> For example, `ghyu.opop.add` in cfg_a can be replaced by the cfg_b in **same** section with the same variable name, while the different namespace keep their variable safely ~ so the value of `ghyu.opop.add` will be 67 and `ghyu.opop.tueo.inpo` refer the flatten variable `inpo` and the value will be 46.

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

---

### **Miscellnous features**
#### **6. IO Converter**
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


#### **7. Absl style flag**
> easy_config also support that you can access the 'same' config file in different python file without re-declare the config. test_flag.py under the same work directory

    from easy_configer.Configer import Configer

    def get_n_blk_from_flag():
        new_cfger = Configer()
        flag = new_cfger.get_cfg_flag()
        # test to get the pre-defined 'n_blk'
        return flag.n_blk

---