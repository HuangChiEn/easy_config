# Project description
#### easy_configer version : 2.2.0

![easy-configer logo](https://raw.githubusercontent.com/HuangChiEn/easy_config/master/assets/logo.png)

---

### Configeruating the program in an easy-way 
I'm willing to provide a light-weight solution for configurating your python program. Hope this repository make every user control their large project more easier ~ ~ 

### Introduction 📝
With the python project go into large-scale, a lot of argument will be required to control the complex business logic, user may need a simple way to load configurations through a file eventually. Their exists various package cover part of function and offer some solution to tackle the mentioned problem. 

**Unfortunately, I can not find a solution for load & use the argument in simple manner at least.**   Instead, most of the config-tools seems only works for the specific goal, then cause the code more longer and hard to read.

For example :
    
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
    

That leverage me to package my solution for solving this issue. The easy_config will cover the following attributes :

1. **simple & customized syntax of declaration (partially support)**

2. **Accept multiple config file in dynamic loading manner**

3. **Declare customized class instance in the config file**

4. **Commend-line update all declared-value wherever it belong, even in hierachical section**

5. **Support the absl style FLAGS functionality** 

6. **Omegaconf like hierachical config**

And, of course the following attribute will also be supported :

* dot-access of any default argument (flatten argument)

* dict-access of any section argument (non-flatten argument) 

* commend-line update any argument value (flatten & non-flatten argument)

* add different settings while choosing to overload previous one.

* inline comment '#', now you can write comment in everyline ~

* support arguments interpolation!!

* support config conversion, which bridge the easy_config into the other config file ~

* support hierachical configurating system with dynamic override ~
---

### Newly update features 🚀
1. Better syntax for override argument via commendline
2. Better syntax for declare the config file
3. Various support of config conversion, including omegaconf, dataclasses, dict, ..., etc.
4. Support enviroment variable (os.Env) interpolation
5. Dynamic sub-config loading..
6. Also update document and some handy examples ~

---

### Bug Fixed 🐛
#### config string with extra space caused config error, and it's fixed in this version.
---

### Dependencies 🏗️
This package is written for Python 3.8. After refactor in this version, this package also support down to python 3.6!!
Of course, light-weight solution **do not** contain any 3-rd package complex dependencies.
The python standard package (such as pathlib, sys, .., etc) is the only source of dependencies, so you don't need to worry about that ~ ~
> However, if you want to use the IO_Converter for converting config into omegaconf, you still need to install omegaconf for this functionality ~

---

### Installation ⚙️<br>
1. **pypi install** <br>
    simply type the `pip install easy_configer` (due to name conflict of pypi pkg, we use different pkg name)
2. **install from source code** <br>
    clone the project from github : `git clone repo-link` 
    Chage to the root directory of the cloned project, and type `pip install -e .`
3. **import syntax** <br>
    Because of the name conflict of pypi pkg, i choice the different pkg name.
    To import the installed pkg, the syntax will be depended on the install method. For example. <br>
    Pip install : `from easy_configer.Configer import Configer` <br>
    git clone & pip install : `from easy_config.Configer import Configer` <br>
    
---

### Quick start 🥂

#### **1. Handy example of config file**
#### Let's say we have an easy-config for development enviroment on jupyter notebook. we want to define several variable for configurating a simple math calculation.

    # config string
    cfg_str = '''
    title = 'math calculation'@str
    coef = 1e-3@float
    with_intercept = True@bool
    intercept = 3@int
    '''

    # look's good, let's get the config!
    from easy_configer.Config import Config
    cfg = Config(description="math calculation config!", cmd_args=False)
    cfg.cfg_from_str(cfg_str)

    # oh.. wait, could we do it more easier ?
    ez_cfg_str = '''
    # opps.. let's change some value
    title = 'linear equation'
    coef = 15        
    '''
    # Note : every time you load the config, if you have the same variable name, 
    #        it will override the value of the variable!
    cfg.cfg_from_str(ez_cfg_str)

    lin_equ = lambda x : cfg.coef * x + cfg.intercept if cfg.with_intercept else (cfg.coef * x)
    x = 15
    print( f"Linear equation with x={x} : { lin_equ(x) }" )


#### In larger project, we may write a config file to control the program, so that the config will become easy to trace, check and debug. In here, we first prepare an config called `test_cfg.ini` in the working directory. 
For easy-config file, there're two type of argument : flatten argument, hierachical argument. You can see that flatten argument is placed in first shallow level, and the argument could be easily accessed by dot operator. Besides flatten argument, all of hierachical argument will be placed in python dict object, thus accessing each argument by key string! 
    
    # ./test_cfg.ini
    # '#' denote comment line, the inline comment is also supported!

    # define 'flatten' arguments :
    serv_host = '127.0.0.1'  
    serv_port = 9478@int    # specific type is also allowed!!
    api_keys = {'TW_REGION':'SV92VS92N20', 'US_REGION':'W92N8WN029N2'}
    
    # define 'hierachical' arguments :
    # the 'section' is the key of accessing dict value and could be defined as follows :
    [db_setup]
        db_host = $serv_host
        # first `export mongo_port=5566` in your bash, then support os.env interpolation!
        db_port = $Env.mongo_port  
        snap_shot = True
    
    # and then define second section for backend server..
    [bknd_srv]
        load_8bit = True
        async_req = True
        chat_mode = 'inference'
        model_type = 'LlaMa2.0'
        [bknd_srv.mod_params]
            log_hist = False
            tempeture = 1e-4
            model_mode = $bknd_srv.chat_mode  # hierachical args interpolation
    
<br>

Now, we're free to launch the chatbot via `python quick_start.py` (*quick_start.py in work directory*)!
However, you can also override the arguemnts via commendline `python quick_start.py serv_port=7894`
    
    import sys
    
    # main_block 
    if __name__ == "__main__":
        from easy_configer.Configer import Configer

        cfger = Configer(description="chat-bot configuration", cmd_args=True)
        # we have defined a config file, let's try to load it!
        cfger.cfg_from_ini("./test_cfg.ini")
        
        # Display the Namespace, it will display all flatten arguemnts and first-level sections
        print(cfger)
        
        ... # for building chat-bot instance `Chat_server`
        chat_serv = Chat_server(host=cfger.serv_host, port=cfger.serv_port, api_keys=cfger.api_keys)

        ... # build mongo-db instance `mongo_serv` for logging chat history..
        mongo_serv.init_setup( **cfger.db_setup )

        ... # loading llm model instance `Llama` ~
        llm_mod = Llama(
            ld_8bit=cfger.bknd_srv.load_8bit, 
            chat_mode=cfger.chat_mode, 
            model_type=cfger.model_type
        )
        llm_mod.init_mod_param( **cfger.bknd_srv['mod_params'] )

        if cfger.bknd_srv['async_req']:
            chat_serv.chat_mod = llm_mod
            chat_serv.hist_db = mongo_serv
        else:
            ... # write sync conversation by yourself..

        sys.exit( chat_serv.server_forever() )

<br>

---

### More detail tutorial about each topic is as follows :

#### **2. How to declare hierachical config**
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

#### **The documentation of easy_configer is also released in read doc** [🔗](https://easy-configer.readthedocs.io/en/latest/)

---

### Simple Unittest 🧪
If you clone this repo and built from source, you can try to run the unittest.
`cd test && python test_Configer.py`

---

### License
MIT License. More information of each term, please see LICENSE.md

### Author 
Josef-Huang, a3285556aa@gmail.com 

### Footer
~ Hope God bless everyone in the world to know his word ~ <br>
**The fear of the LORD is the beginning of knowledge; fools despise wisdom and instruction. by Proverbs 1:7**