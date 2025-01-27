# Project description
#### easy_configer version : 2.5.6
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/HuangChiEn/easy_config/main.yaml)
[![PyPI version](https://badge.fury.io/py/easy-configer.svg?icon=si%3Apython)](https://badge.fury.io/py/easy-configer)
[![Documentation](https://img.shields.io/badge/documentation-link-blue.svg)](https://easy-configer.readthedocs.io/)

![easy-configer logo](https://raw.githubusercontent.com/HuangChiEn/easy_config/master/assets/logo.png)

---

### TODO list :
0. Next version v3.0 is under development, stateless interface will be introduced as one of new features
1. Known issue : commendline argument will not update sub_config arguments, will be fixed in v3.0
2. Nested argument intepolation may be one of features in v3.0
3. You can preview the v3.0 prototype of codebase under ./dev folder 

---
### Package demo ~
https://github.com/user-attachments/assets/1d6f43a4-f621-433c-a6c0-d267c7b32399
> The demo video only cover basic functionality of easy_configer, more examples plz refer the doc below..

---

### Configeruating the program in an easy-way 
I'm willing to provide a light-weight solution for configurating your python program. Hope this repository make every user control their large project more easier ~ ~ 

### Easy-configer document
**Check the documentation released in ReadTheDoc[🔗](https://easy-configer.readthedocs.io/en/latest/), to learn more!**

Easy-config cover the following features :
1. **Hierachical section config (nested dict-like config)**

2. **Accept multiple config file in dynamic loading manner (similar with omegaconf)**

3. **Support customized class (initialized by list or keyword arguments)**

4. **Commend-line add/update declared arguments/sections (even in hierachical section)**

5. **Support the absl style FLAGS functionality (declare once, use anywhere)** 

And, of course the following attributes are supported :

* dot-access of any config argument (even in nested dictionary)

* inline comment '#', now you can write comment in everyline ~

* support config argument interpolation (even in nested dictionary)!

* support config conversion, feel free to use easy_config or the other config tools (omegaconf, argparse, ..., etc.)

* support omegaconf-like dynamic config loading system ~

---

### Newly update features 🚀
0. v2.5.4 is basically stable, but we add more test case in this version (it's more stable now) ~
1. Apply ${cfg}, ${env} as argument and enviroment intepolation notation, respectively.
2. Apply AttributeDict container (it inherit pure python dict) to store non-flatten arguments!

---

### Bug Fixed 🐛
#### Hot-fix Container bug in v2.5.3, now it'll raise AttributeError while attribute doesn't exists..(fixed in v2.5.4)

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
    clone the project from github : `git clone https://github.com/HuangChiEn/easy_config.git` 
    Chage to the root directory of the cloned project, and type `pip install -e .`

3. **import syntax** <br>
    Wherever you install, pypi or source. Now, you just need a simple import : `from easy_configer.Configer import Configer`
    
---

### Quick start 🥂

#### **1. Handy example of config file**
Let's say we have an easy-config for development enviroment on jupyter notebook. we want to define several variable for configurating a simple math calculation.

```python
# config string
cfg_str = '''
title = 'math calculation'@str
coef = 1e-3@float
with_intercept = True@bool
intercept = 3@int
'''

# look's good, let's get the config!
from easy_configer.Configer import Configer
# `cmd_args=False` disable any commendline args 
cfg = Configer(description="math calculation config!", cmd_args=False)
cfg.cfg_from_str(cfg_str)

# oh.. wait, could we do it more easier ?
ez_cfg_str = '''
# opps.. let's change some value
title = 'linear equation'
coef = 15        
'''
# By default, we don't encourage you to overwrite the predefined arguments,  
#        if you want to overwrite it in 'convenient way', you should set `allow_overwrite=True`..
cfg.cfg_from_str(ez_cfg_str, allow_overwrite=True)

lin_equ = lambda x : cfg.coef * x + cfg.intercept if cfg.with_intercept else (cfg.coef * x)
x = 15
print( f"Linear equation with x={x} : { lin_equ(x) }" )
```
> If you want to overwrite previous config, *apply twice* `cfg.cfg_from_str` with `allow_overwrite=True` flag IS NOT a recommended way. In easy-configer, we provide 2 way to do that. The standard way is *declaring 2 config and apply config merging method* to get the updated config. The other way is similar with omegaconf to import sub-config in dynamic manner,  however you still need to set flag `allow_overwrite=True` in `cfg.cfg_from_ini`.

Although writing a string config in python is convenient, it only suitable for the project in smaller scale. In large project, we may write a config file to control the program, so that we will be easy to trace, check and debug the config. We are going to prepare a sample config called `test_cfg.ini` in the working directory and describe how we work with chatbot roughly. 

#### In easy-configer, there're two type of argument in config : flatten argument, hierachical argument. You will see that the flatten arguments are directly placed in config and doesn't belong any section (namely in first level). In contrast, the hierachical arguments will be placed in section (i.e. `[db_setup]`) with any kind of depth, the arguments under the section will be wrapped by a container (`easy_configer.utils.Container.AttributeDict`) similar with pure python `dict`. 

#### To form a hierachical argument in nested section, we apply toml-like syntax to describe the nested section (i.e. `[bknd_srv.mod_params]` is belong to `[bknd_srv]` parent section). The arguments in nested section are also wrapped by nested AttributeDict. Besides you can access all kind of arguments by the simple dot-operator, however, we still recommend you to use key-string as pure python dict.
> Note that the recommended way to access the argument is **still** key-string access `cfger.args['#4$%-var']`, as you may notice, dot-access doesn't support **ugly** variable name (`cfger.#4$%-var`, as variable name is invalid in python intepreter). 
    
```ini
# ./test_cfg.ini
# '#' denote comment line, the inline comment is also supported!

# define 'flatten' arguments :
serv_host = '127.0.0.1'  
serv_port = 9478@int    # specific type is also allowed!!
api_keys = {'TW_REGION':'SV92VS92N20', 'US_REGION':'W92N8WN029N2'}

# define 'hierachical' arguments :
# the 'section' is the key of accessing AttributeDict's value and could be defined as follows :
[db_setup]
    db_host = ${cfg.serv_host}:80@str
    # first `export mongo_port=5566` in your bash, then support os.env interpolation!
    db_port = ${env.mongo_port}  
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
        model_mode = ${cfg.bknd_srv.chat_mode}  # hierachical args interpolation
```

<br>

Now, we're free to launch the chatbot via `python quick_start.py` (*quick_start.py in work directory*)!
However, you can also overwrite the arguemnts via commendline `python quick_start.py serv_port=7894 bknd_srv.chat_mode=predict@str`
> Note that **update argument** from commendline is naturally permitted, but overwrite **the section** IS NOT! If you also want to overwrite the section, you need to set flag `allow_overwrite=True`. 

```python
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
    # un-roll section arguments as unzip python dict for kwargs ~
    mongo_serv.init_setup( **cfger.db_setup )

    ... # loading llm model instance `Llama` ~
    llm_mod = Llama(
        ld_8bit=cfger.bknd_srv.load_8bit, 
        chat_mode=cfger.chat_mode, 
        model_type=cfger.model_type
    )

    # you can access nested-dict by dot access ~
    llm_mod.init_mod_param( **cfger.bknd_srv.mod_params )

    # or you can keep the dict fashion ~
    if cfger.bknd_srv['async_req']:
        chat_serv.chat_mod = llm_mod
        chat_serv.hist_db = mongo_serv
    else:
        ... # write sync conversation by yourself..

    sys.exit( chat_serv.server_forever() )
```

<br>

---

### More detail tutorial about each topic is as follows :

#### **2. How to declare hierachical config**
There have two kind of way to prepare the arguments in easy-configer as we described. In practices, we consider the flatten arguments as global setup, and grouping the rest of arguments into the corresponding section for assigning it according to the subroutine.  

Let's give a deep-learning example, suppose you have created a *hier_cfg.ini in work directory*
```ini
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
```

We have defined the config file, **now let's see how to access any argument!** Execute `python quick_hier.py` in work directory.

```python
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
```

However, the syntax in config could be improved, isn't it !? For example, *the batch_size is defined twice under `dataset.loader` and `train_cfg`, so as layer seed.* Moreover, *path is defined as python string, it need to be further converted by Path object* in python standard package. Could we regist our customized data type for easy-config ?
#### Glade to say : Yes! it's possible to elegantly deal with above mentioned issue. We can solve the first issue by using argument interpolation, and solve the second issue by using the customized register!!

#### Thanks to *python format-string ${...}* and  *customized register method `regist_cnvtor`*. **See below example**
> Currently we support interpolation mechanism to interpolate *ANY* arguemnts even beloning to nested section by simply using **\${cfg}** notation. Moreover, we also support **\${env}** for accessing enviroment variables exported in bash!!

```python
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
```

---

#### **3. Access all arguments flexibly**
For `easy_configer>=v2.4.0`, each argument declared under section will be stored in a special dictionary object, called `AttributeDict` (Inhert from native python `dict`). It's a new container allowing dot-operator for accessing any nested object.
The only pitfall about AttributeDict is that **you should never access its `__dict__` property**, since it's disabled..
We simple set a breakpoint to feel how flexible does `easy_configer.utils.Container.AttributeDict` support.

```python
from easy_configer.Configer import Configer

if __name__ == "__main__":
    cfger = Configer()
    cfger.cfg_from_ini("./hier_cfg.ini")
    breakpoint()
```
> We write a special example `hier_cfg.ini`!!
```ini
# nested-dict
[secA] # test depth ((sub^4)-section under secA)
    lev = 1
    [secA.secB]
        lev = 2
        [secA.secB.secC]
            lev = 3
            [secA.secB.secC.secD]
                lev = 4
```
Now you can access each `lev` :
1. `(pdb) cfger.secA.lev `, output `lev : 1`
2. `(pdb) cfger['secA'].secB['lev'] `, output `lev : 2`, and so on..
3. Most crazy one ~ `(pdb) cfger.secA.['secB'].secC['secD'].lev `, output `lev : 4`

---

#### **4. Commmend-line Support**
> We also take `hier_cfg.ini` as example!
```ini
# hier_cfg.ini
glb_var = 42@int
[dataset]         
    ds_type = None
    path = ['/data/kitti']@pyPath
    [dataset.loader]
        batch_size = 32@int
```

Execute python program and print out the helper information <br>
`python quick_hier.py -h`

Update flatten argument and print out the helper information <br>
`python quick_hier.py glb_var=404 -h`

Especially update **non-flatten argument**, you can access any argument at any level by dot-access in commend-line!! (with combining any argument update). Now, try to change any nested argument <br>
`python quick_hier.py dataset.ds_type="'kitti'" dataset.path=['/root/ds'] dataset.loader.batch_size=48`

( Note that the commendline declaration for string is tricky, but currently we only support two way for that : 
    `dataset.ds_type="'kitti'"` or `dataset.ds_type=kitti@str`, pick up one of you like ~ )

---

#### **5. Import Sub-Config**
Like `omegaconf`, most of user expect to seperate the config based on their category and dynamically merge it in runtime. It's a rational requirement and the previous version of easy-config provide two way to conduct it, but both have it's limit : 
1. you can call the `cfg_from_ini` twice, for example, `cfg.cfg_from_ini('./base_cfg') ; cfg.cfg_from_ini('./override_cfg', allow_overwrite=True)`. But it's not explicitly load the config thus reducing readability.
2. you can use the config merging, for example, `new_cfg = base_cfg | override_cfg`. But it's not elegant solution while you have to merge several config..

#### Now, we provide the thrid way : **sub-config**. you can import the sub-config in any depth of hierachical config by simply placing the `>` symbol at the beginning of line. Also note that sub-config doesn't allow you overwrite the section by default, since dynamically overwrite the section is not necessary generally (also made your config hard to trace).

```ini
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
```

#### Also note that we still recommend you create several config instance and merge it in 2. way, if you want to merge it with overwriting manner. Instead of acting like omegaconf, it dynamically overwrite your config silently..
> If you **still** want to overwrite the config (act like omegaconf), turn the flag allow_overwrite as True. i.e. `cfg.cfg_from_ini(..., allow_overwrite=True)`, `cfg.cfg_from_str(..., allow_overwrite=True)`. The sub-config will follow the flag setting to overwrite the config. Be careful of the order, the **imported sub-configs** are considered as **'default setup'**, the main config (which import sub-configs) setup will overwrite its.  

```ini
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
```

#### After dynamic loading :
```ini
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
```

---

#### **6. Config Operation**
Config operation is one of the core technique for dynamic configuration system!!
In the following example, you can see that the merging config system already provided a impressive hierachical merging funtionality! 
> For example, `ghyu.opop.add` in cfg_a can be replaced by the cfg_b in **same** section with the same variable name, while the different namespace keep their variable safely ~ so the value of `ghyu.opop.add` will be 67 and `ghyu.opop.tueo.inpo` refer the flatten variable `inpo` and the value will be 46.

```python
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
    
    # default, overwrite falg is turn off ~
    cfg_a.merge_conf(cfg_b, overwrite=True)

    # `cfg_b = cfg_b | cfg_a`, operator support, warn to decrease the read-ability...
    # cfg_a will overwrite the argument of cfg_b which share the identitical variable name in cfg_b!
    # operator support : `cfg_b |= cfg_a` == `cfg_b = cfg_b | cfg_a`
```

---

### **Miscellnous features**
#### **7. IO Converter**
To convert the `easy_configer` type config into the other config instance, we provide a IO converter to serve for this requirement. IO converter support several well-know config type.. Just simple call the method with the proper arguments as the following example. 

```python
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
```

---

#### **8. Absl style flag**
easy_config also support that you can access the 'same' config file in different python file without re-declare the config. utils.py under the same work directory

Suppose you have executed `main.py`:
```python
from easy_configer.Configer import Configer
from utils import get_var_from_flag

if __name__ == "__main__":
    cfg = Configer()
    cfg.cfg_from_str("var = 32")

    # both should output 32 ~
    print(f"var from main : {cfg.var}")
    print(f"var from flag : { get_var_from_flag() }")
```

Now, when you step in `get_var_from_flag` function in different file..
```python
from easy_configer.Configer import Configer

def get_var_from_flag():
    new_cfger = Configer()
    flag = new_cfger.get_cfg_flag()
    # test to get the pre-defined 'var'
    return flag.var
```
---

### Simple Unittest 🧪
If you clone this repo and built from source, you can check the unittest.
`python -m unittest discover`
> I have placed all test file under test folder.

---

### License
MIT License. More information of each term, please see LICENSE.md

### Author 
Josef-Huang, a3285556aa@gmail.com 

### Footer
~ Hope God bless everyone in the world to know his word ~ <br>
**The fear of the LORD is the beginning of knowledge; fools despise wisdom and instruction. by Proverbs 1:7**
