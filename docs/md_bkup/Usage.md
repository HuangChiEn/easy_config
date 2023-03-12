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


#### **2. Absl style flag**
> easy_config also support that you can access the 'same' config file in different python file without re-declare the config. test_flag.py under the same work directory

    from easy_configer.Configer import Configer

    def get_n_blk_from_flag():
        new_cfger = Configer()
        flag = new_cfger.get_cfg_flag()
        # test to get the pre-defined 'n_blk'
        return flag.n_blk

        
#### **3. Commmendline Support**

Execute python program and print out the helper information <br>
`python quick_start.py -h`

Update flatten argument and print out the helper information <br>
`python quick_start.py -n_blk 400 -h`

Especially update **non-flatten argument !!** <br>
`python quick_start.py --fir_sec-dummy_val 45 -n_blk 400 -h`

#### **4. IO Converter**

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

---