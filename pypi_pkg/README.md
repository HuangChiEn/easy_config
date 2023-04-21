# Project description
#### easy_configer version : 2.0.1

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

2. **Accept multiple config file with dynamic style**

3. **Declare customized class instance in the config file**

4. **Commend-line update all declared-value wherever it belong**

5. **Support the absl style FLAGS functionality** 

6. **Omegaconf like hierachical config**

And, of course the following attribute will also be supported :

* dot-access of any default argument (flatten argument)

* dict-access of any section argument (non-flatten argument) 

* commend-line update any argument value (flatten & non-flatten argument)

* add different settings while choosing to overload previous one.

* inline comment '#', now you can write comment in everyline ~

* support arguments (flatten) interpolation!!

* support config conversion, which bridge the easy_config into the other config file ~

* support hierachical configurating system with dynamic override ~
---

### Newly update features 🚀
1. Eventually, we have support hierachical configuration. **So, you can define hierachical config (beyond two-level) with toml-like section. Easy_configer now support this feature and convert your hierachical declearation into the hierachical dict structure.** Have a look at documentation!! 

2. Along with the new feature : hierachical config, we also support the commend-line override with any value declared in any layer of config!! **it's not easy, but we did it www.** Have a look at documentation!!

3. Config merging mechnaism is a common technique in dynamic configuration. **So, we also support config merging in this version!!** yeah ~ feel free to merg, concat, and then override the config to make your python program more controllable!!
---

### Bug Fixed 🐛
#### No bug report in previous version, feel free to report the bug via issue on github.
---

### Dependencies 🏗️
This package is written for Python 3.8 (but 3.6+ may be supported).
Of course, light-weight solution **do not** contain any 3-rd package complex dependencies.
The python standard package (such as pathlib, sys, .., etc) is the only source of dependencies, so you don't need to worry about that ~ ~
> However, if you want to use the IO_Converter (config conversion mechnaism), you still need to install omegaconf for integrate with hydra ~

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

#### **1. How to write config file**

#### *test_cfg.ini in work directory*
    
    # '#' denote comment line
    # below define default argument, which is called 'flatten' args
    luck_num = 42@int  # now we also support inline comment.. finally
    name = Harry@str
    even_mk_dict = {'a':123, 'b':'string'}@dict
    
    # Well-define config file may use 'section' to split the args
    # and the section can be defined as follows :
    [fir_sec]
    dummy_val = 78.5@float
    
    # and then define second section 
    [sec_sec]
    dummy_val = 45@int
    
    # finall, you will find that, configer isolate the namespace 
    # to store the values with the corresponding section name.
    # So, 2 dummy_val will not conflict with different section.
    
<br>

#### *quick_start.py in work directory*
    
    # Epilog
    from easy_configer.Configer import Configer
    # new feature!! suport flag
    from test_flag import get_n_blk_from_flag

    # Of course, you can simple make the config file with the simple string, 
    # which is very suitable for cell-based development enviroment (e.g. jupyter-lab)
    # Do not forgot, always declare cfg_str in global part, not in main_block 
    # By the way, you're allowed to define section-params in the cfg-str,
    #   however, it's not recommend due to it's readibility!!
    cfg_str = '''
    lr = 1e-4@float
    n_blk = 5@int
    tst_var = {'num':3, 'name':'joseph'}@tst_cls
    '''
    
    class Test(object):    
        def __init__(self, num, name):
            self.num = num
            self.name = name

        def num_name(self):
            return self.num * self.name
    
    # main_block 
    if __name__ == "__main__":
        cfger = Configer(description="helper information string in cmdline", cmd_args=True)
        cfger.regist_cnvtor("tst_cls", Test)  # regist customer class 
        
        # Feed 2 different config file into Configer..
        cfger.cfg_from_str(cfg_str)
        cfger.cfg_from_ini("./test_cfg.ini")
        
        # Display the Namespace 
        print(cfger)
        # Get the flatten argument
        print(cfger.n_blk)
        print( type(cfger.test) )  # chk the type!
        # test the customized class
        print(cfger.tst_var.num_name())
        # test the flag 
        print(get_n_blk_from_flag())
        
        # Get the non-flatten argument
        assert cfger.fir_sec['dummy_val'] != cfger.sec_sec['dummy_val']
        
        print( type(cfger.sec_sec['dummy_val']) )

<br>

#### *config interpolation with $ symbol*
> Currently we support simple interpolation mechnaism, which only allow the *intepolated args* be putted in the **flatten section**. (you **cannot** interpolate args from **non-flatten section**)

    def get_str_cfg():
        '''
            # flatten section, you can put shared args
            shr_port = 5566@int

            [sec_A]
                inner_port = $shr_port
            [sec_B]
                outter_port = $shr_port
        '''

    # main_block 
    if __name__ == "__main__":
        cfger = Configer(description="sample for arguments interpolation")

        cfg_str = get_str_cfg()
        cfger.cfg_from_str(cfg_str)
        
        # Shared port
        print(cfger.shr_port)
        # Assert
        print(cfger.sec_A['inner_port'] == cfger.shr_port)
        print(cfger.sec_A['inner_port'] == cfger.sec_B['outter_port'])

#### **2. How to declare hierachical config**

#### *hier_cfg.ini in work directory*
    glb_var = 42@int
    [dataset]         
        sample_seed = $glb_var
        path = {'root':'/data/kitti'}@Path
        [dataset.loader]
            batch_size = 32@int

    [model]
        [model.backbone]
             = 32@int
            [model.backbone.optimizer]
                lay_seed = $glb_var   # intepolation to any sub-section!
                lr = 1e-4@float

    # Hier-Cell cfg written by Josef-Huang..

#### *quick_hier.py in work directory*

    from easy_configer.Configer import Configer
    from pathlib import Path
    
    if __name__ == "__main__":
        cfger = Configer(cmd_args=True)
        cfger.regist_cnvtor("Path", Path)
        
        # omit cfg_from_str, hier-config also could be declared in str though ~
        cfger.cfg_from_ini("./hier_cfg.ini")
        
        # Display the Namespace 
        print(cfger)
        print(cfger.dataset)
        
        some_dataloader_func(**cfger.dataset['loader'])

        print(cfger.model['backbone']['optimizer'])


#### **3. Commmend-line Support**
> We also take `hier_cfg.ini` as example!

    # hier_cfg.ini
    glb_var = 42@int
    [dataset]         
        sample_seed = $glb_var
        path = {'root':'/data/kitti'}@Path
        [dataset.loader]
            batch_size = 32@int

    [model]
        [model.backbone]
             = 32@int
            [model.backbone.optimizer]
                lay_seed = $glb_var   # intepolation to any sub-section!
                lr = 1e-4@float

    # Hier-Cell cfg written by Josef-Huang..

Execute python program and print out the helper information <br>
`python quick_hier.py -h`

Update flatten argument and print out the helper information <br>
`python quick_hier.py -glb_var 404 -h`

Especially update **non-flatten argument**, you can access any argument at any level by dot-access in commend-line!! (with combining any argument update)<br>
`python quick_start.py -model.backbone.optimizer.lr "{'yeah':'success'}@dict" -dataset.sample_seed 578@int -h`

#### **4. Config Operation**
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
        # operator support : cfg_b |= cfg_a

---

### **Miscellnous features**
#### **5. IO Converter**

    # first import the IO_converter
    from easy_config.IO_Converter import IO_Converter
    cfg_cnvter = IO_Converter()

    # convert easy_config instance into the argparse instance
    argp_cfg = cfg_cnvter.cnvt_cfg(self.cfger, 'argparse')

    uargp_cfg = cfg_cnvter.cnvt_cfg(self.cfger, 'argparse', parse_arg=False)
    argp_cfg = uargp_cfg.parse_args()

    # convert easy_config instance into the omegaconf instance
    ome_cfg = cfg_cnvter.cnvt_cfg(self.cfger, 'omegacfg')

    # convert easy_config instance into the "yaml string"
    yaml_cfg = cfg_cnvter.cnvt_cfg(self.cfger, 'yaml')


#### **6. Absl style flag**
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