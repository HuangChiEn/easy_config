# Project description
### Configeruating the program in an easy-way
This is a light-weight solution for configurating the python program. <br>
Hope this repository make every user control their large project with easier ~ ~ 

### Introduction
With the large python project, a lot of argument will be required to control the business logic, user may need a simple way to load configurations through a file eventually. Their exists various package cover part of function with each other, and offer some solution to tackle the mentioned problem. 

**But at least I can not find a solution for load & use the argument in simple manner.**   Instead, most of them seems for the specific goal, and cause the code more longer and hard to read.

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
    

That's why I packaged my solution to this issue. The easy_config will have following attribute :

1. **simple & customized syntax of declaration (partially support)**

2. **Accept multiple config file with dynamic style**

3. **Declare customized class instance in the config file (partially support)**

4. **Commend-line update default value**

5. **Support the absl style FLAGS functionality** 

And, of course the following attribute will also be supported :

* dot-access of any default argument (flatten argument)

* dict-access of any section argument (non-flatten argument) 

* commend-line update any argument value (flatten & non-flatten argument)

* add different settings while choosing to overload previous one.

* inline comment '#', now you can write comment in everyline!!
---

### Newly update features 🚀
1. inline comment '#' is now avaliable!!

2. simple unittest can be exec `cd test ; python test_Configer.py`

3. Better error message about the invalid configuration is given by Configer..
---

### Bug Fixed 🐛
1. Bug of bool type variable declaration is fixed, now 'False' will give exactly 'False'

### Dependencies
This package is written for Python 3.8 (but 3.6+ may be supported).
Of course, light-weight solution **do not** contain any 3-rd package complex dependencies.
The python standard package (such as pathlib, sys, .., etc) is the only source of dependencies, so you don't need to worry about that ~ ~

### Installation <br>
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

### Quick start

#### How to write config file -

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
    #   however, it's not recommend due to it's readibility..
    !!
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

#### In the new feature -- absl style flag, easy_config also support that you can access the 'same' config file in different python file without re-declare the config..
> test_flag.py under the same work directory

    from easy_configer.Configer import Configer

    def get_n_blk_from_flag():
        new_cfger = Configer()
        flag = new_cfger.get_cfg_flag()
        # test to get the pre-defined 'n_blk'
        return flag.n_blk

        
#### *Finally, cmd-support*

Execute python program and print out the helper information <br>
`python quick_start.py -h`

Update flatten argument and print out the helper information <br>
`python quick_start.py -n_blk 400 -h`

Especially update **non-flatten argument !!** <br>
`python quick_start.py --fir_sec-dummy_val 45 -n_blk 400 -h`


**For more information, please check the document, it maybe release in next version**

---

### Simple Unittest
If you clone this repo and built from source, you can try to run the unittest.
`cd test && python test_Configer.py`

### License
MIT License. More information of each term, please see LICENSE.md

### Author 
Josef-Huang, a3285556aa@gmail.com 

### Footer
~ Hope God bless everyone in the world to know his word ~ <br>
**The fear of the LORD is the beginning of knowledge; fools despise wisdom and instruction. by Proverbs 1:7**