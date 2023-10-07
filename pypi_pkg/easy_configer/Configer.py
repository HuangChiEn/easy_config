import errno
import os
import sys
from copy import deepcopy
from pathlib import Path

import warnings
def warning_on_one_line(message, category, filename, lineno, file=None, line=None):
    return "{0}:{1}: {2}: {3}\n".format(filename, lineno, category.__name__, message)
warnings.formatwarning = warning_on_one_line

from .utils.Type_Convertor import Type_Convertor
from .utils.Flag import Flag
from .IO_Converter import IO_Converter

class Configer(object):
    '''
        The Configer attemtp to make a light-weight solution for configurating your program, 
        which offer a simple syntax for declare the arguments in the configure file (.ini suffix).
        Moreover, I try to implement a highly customer reader, which allow the user to declare 
        the instance of customer class with registered their constructor simply. 
        
        Hope such trivial contribution will let your work become easier ~ ~ God bless you.
    '''
    def __init__(self, description:str = "", cmd_args:bool = False, split_chr:str = " = "):
        '''
            description (option) : 
                A customer helper information which describe the functionality of your configer file.
            
            cmd_args (option) :
                Allow the commend line argument update the declared value of configer file.
                
            declare_split_chr (option) :
                The character make use to split the declaration string in configer file.
                For example, 'a*13@int' which means the argument 'a' contain interger value 13,
                and the '*' is the declare_split_chr.
        '''
        self.__doc_str = "Description : \n" + description
        self.__typ_cnvt = Type_Convertor()
        self.__cfg_cnvt = IO_Converter()
        self.__split_chr = split_chr
        self.__flag = Flag().FLAGS
        self.__cmd_args = cmd_args

    ## Main interface for configuration : 
    # Support commendline config
    def cfg_from_cli(self):
        ''' 
            The commendline-based configuration, specific arguments from commend-line only.
            ( only recommend for very lightweight config ) 
        '''
        if not self.__cmd_args:
            warnings.warn("'cfg_from_cli' is called, the settings 'cmd_args=False' will be ignored!")
        self.args_from_cmd()
            
    # Support string config in cell-based intereactive enviroment
    def cfg_from_str(self, raw_cfg_text:str):
        ''' 
            raw_cfg_text :
                The string which declare the arguments with the same syntax used in config file. 
        '''
        self.__cfg_parser(raw_cfg_text)
        # build the flag object 
        self.__flag.__dict__ = self.__dict__
    
    # Load .ini config from the given path
    def cfg_from_ini(self, cfg_path:str):
        '''
            cfg_path :
                The path which locate the '*.ini' config file.
        '''
        def chk_src(cfg_path):
            if not cfg_path.exists():
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), str(cfg_path))
            if not cfg_path.suffix == ".ini":
                raise ValueError("The file extension should be 'ini', instead of '{0}'".format(cfg_path.suffix))
            
        try:
            # check config path validation
            cfg_path = Path(cfg_path)
            chk_src(cfg_path)

            with cfg_path.open('r') as cfg_ptr: 
                raw_cfg_text = cfg_ptr.read()
            
        except FileNotFoundError as fnf_err:
            print(fnf_err) ; raise
        except ValueError as val_err:
            print(val_err) ; raise
        except PermissionError as per_err:
            print(per_err) ; raise
        except Exception as ex:
            print(ex) ; raise
        else:
            self.__cfg_parser(raw_cfg_text)
        
        # build the flag object 
        self.__flag.__dict__ = self.__dict__
    
    ## Core implementation of config parser : 
    #  utils of config parser
    def __preproc_cfgstr(self, cfg_str:str) -> str:
        # eliminate the line full of white-space without any text
        cfg_str = cfg_str.strip() 
        # skip empty line and comment line 
        if len(cfg_str) == 0 or cfg_str[0] == '#': 
            return ''
        # strip inline comment's content with strip extra-whitespace
        return cfg_str.split('#')[0].strip()

    def __get_sec(self, cfg_str:str) -> str:
        if '[' != cfg_str[0]:
            return ''
        # more robust with Indented section
        beg, end = cfg_str.find('['), cfg_str.rfind(']')
        if end == -1:
            raise RuntimeError("Configuration Error : Invalid section notation, missing ']' at end of line")
        sec_key_str = cfg_str[beg+1 : end].strip()
        return sec_key_str
    
    def __idx_sec_by_dot(self, sec_keys_str:str, allow_init:bool = False) -> [dict, str]:
        '''
            Core function to manage the hierachical arguments. 
            Store args is simple, just add it in dict. But dynamically search argument in specific section is non-trivial!
            Therefore, i wrote this function to deal with searching and return the "pointer" point to the section.
            It's sync with self.__dict__, so use it wiselly & carefully!!
        '''
        sec_name_lst = sec_keys_str.split('.')
        # Before easy_configer 1.3.4 ver, all section is builded upon this level
        if len(sec_name_lst) == 1:
            return self.__dict__, sec_keys_str

        root_key = sec_name_lst.pop(0)
        if root_key not in self.__dict__:
            if not allow_init:
                raise RuntimeError("The parent node of {0} is not defined yet, " \
                                        "it's invalid for directly made the child node".format(root_key))
            self.__dict__[root_key] = {}

        ## Support toml like 'hierachical' format!!
        #  dynamically search the hierachical section begin from the 'next layer' of self.__dict__
        idx_sec = self.__dict__[root_key]
        #  keep the index point to the node "parent", since the child node will be init as dict!
        for sec in sec_name_lst[:-1]:
            tmp = idx_sec.get(sec, '__UNDEFINE_VAL')
            if tmp == '__UNDEFINE_VAL':
                if not allow_init:
                    raise RuntimeError("The parent node '{0}' is not defined yet, " \
                                            "it's invalid for directly made the child node".format(sec))
                idx_sec[sec] = {}
            idx_sec = idx_sec[sec]

        return idx_sec, sec_name_lst[-1]

    def __get_declr_dict(self, cfg_str:str) -> dict : 
        if self.__split_chr not in cfg_str:
            raise RuntimeError("Configuration Error : Split character '{0}'" \
                                " not found in '{1}'".format(self.__split_chr, cfg_str))
        
        try:
            var_name, val_str = cfg_str.split(self.__split_chr)
            # support '$' notation for hierachical args interpolation!
            if val_str[0] == '$':
                val_str = val_str[1:]
                if 'ENV' in val_str:   # to be honest, i don't think we should have to resolve complex object except os.env
                    env_key = val_str.split('.')[-1]
                    intep_val = os.environ[env_key]
                else:    
                    sec_ptr, sec_key = self.__idx_sec_by_dot(val_str)
                    intep_val = sec_ptr[sec_key]
                var_val = intep_val
            else:
                var_val = self.__typ_cnvt.convert(val_str)
        except:
            raise RuntimeError("Configuration Error : Invalid config string ' {0}' ".format(cfg_str))

        return { var_name : var_val }

    # core function of config parser
    def __cfg_parser(self, raw_cfg_text:str):
        '''
            raw_cfg_text :
                The string which declare the arguments with the same syntax used in config file.
        '''

        def parse_sub_config(sub_cfg_path:str):
            '''
                sub_cfg_path :
                    The path of interpolated config. 
                    The sub-config path is parsed from the .ini file with split '>' symbol.
            '''
            sub_cfg = Configer(cmd_args=False)
            sub_cfg.cfg_from_ini(sub_cfg_path)
            return self.__cfg_cnvt.cnvt_cfg_to(sub_cfg, 'dict')

        cur_sec_keys = ''
        for lin in raw_cfg_text.splitlines():
            # strip empty space and 'skip' empty line in cfgstr
            cfg_str = self.__preproc_cfgstr(lin)
            if not cfg_str:
                continue

            # get the section key of config string (if there exists)
            sec_keys_str = self.__get_sec(cfg_str)
            if sec_keys_str:
                idx_sec, idx_sec_key = self.__idx_sec_by_dot(sec_keys_str)
                if idx_sec_key in idx_sec.keys():
                    raise RuntimeError('Re-defined config, {0} section will be overrided!!'.format(sec_keys_str))
                idx_sec[idx_sec_key] = {}
                cur_sec_keys = sec_keys_str
            
            # parse variable assignment string
            else:
                # parse the value string into value dict
                if cfg_str[0] == '>':
                    # import other .ini config as value dict
                    sub_cfg_path = cfg_str.split('>')[-1].strip()
                    val_dict = parse_sub_config(sub_cfg_path)
                else:
                    # normal value string
                    val_dict = self.__get_declr_dict(cfg_str)

                # assign the val_dict into the corresponding section!
                if cur_sec_keys != '':
                    idx_sec, idx_sec_key = self.__idx_sec_by_dot(cur_sec_keys)
                    idx_sec[idx_sec_key].update( val_dict )
                else:
                    self.__dict__.update( val_dict )

        # Update the namespace value via commend-line input 
        if self.__cmd_args:
            self.args_from_cmd()

    def args_from_cmd(self):   
        '''
            Update the arguments by commend line input string
        '''
        # remove file name from args
        cmd_arg_lst = sys.argv[1:]
        
        # print out helper document string
        if "-h" in cmd_arg_lst:
            cmd_arg_lst.remove("-h")
            print(self.__doc_str)

        # ' = ' -> '=', eliminate white space
        cmd_sp_chr = self.split_char.strip()
        sec_ptr, sec_key = None, None
        for item in cmd_arg_lst:
            itm_lst = [ itm for itm in item.split(cmd_sp_chr) if itm != '']
            if len(itm_lst) != 2:
                raise RuntimeError(f"Invalid commendline input : the split char '{cmd_sp_chr}' should only present once and the value should be given!")
            
            sec_keys_str, val_str = itm_lst
            sec_ptr, sec_key = self.__idx_sec_by_dot(sec_keys_str, allow_init=True)
            sec_ptr[sec_key] = self.__typ_cnvt.convert(val_str)

    ## Configuration operator support :
    #  all of operator will be forced to return value!!
    #   merge operator, force to override!
    def __or__(self, cfg):
        cp_cfg = deepcopy(self)
        cp_cfg.merge_conf(cfg, override=True)
        return cp_cfg

    #   concate operator 
    def __add__(self, cfg):
        return self.concate_cfg(cfg)

    # concate just means merge2conf "without" any override!!
    def concate_cfg(self, cfg):
        cp_cfg = deepcopy(self)
        cp_cfg.merge_conf(cfg, override=False)
        return cp_cfg
        
    #   merge conf suppose 2 config have overlap section, otherwise use 'concate' method!
    def merge_conf(self, cfg, override=True):
        
        def hier_merge(sf_dict, cfg_dict):
            for sec_key, sec_val in cfg_dict.items():
                # same section exists
                if sec_key in sf_dict.keys():
                    if not override:
                        raise RuntimeError("Key '{0}' in input config already exists in merged config!!".format(sec_key))
                    
                    # if both self-dict and cfg_dict are dict, merge it hierachically!
                    if isinstance(sec_val, dict) and isinstance(sf_dict[sec_key], dict):
                        hier_merge(sf_dict[sec_key], sec_val)
                    else:
                        sf_dict[sec_key] = sec_val

                # directly feed new val
                else:
                    sf_dict[sec_key] = sec_val

        # prevent checking private vars
        cfg_dict = { k:v for k, v in cfg.__dict__.copy().items() \
                                    if '_' != k[0] }
        hier_merge(self.__dict__, cfg_dict)

    # Display the namespace which record all of the declared arguments
    #   for the inner-node structure, iter-call __str__ wrapper !!
    def __str__(self):
        key_str = [ str(key) for key in self.__dict__.keys() if key[0] != '_' ] 
        return "Namespace : \n" + ", ".join(key_str)
    # override default __repr__ to view configer in debugger
    __repr__ = __str__
    
    ## Miscellnous functionality : 
    # return an absl style flag to store all of the args.
    def get_cfg_flag(self):
        return self.__flag

    def get_doc_str(self):
        return self.__doc_str

    # For the declare the instance of user customized class 
    def regist_cnvtor(self, *args:list, **kwargs:dict):
        self.__typ_cnvt.regist_cnvtor(*args, **kwargs)
    
    # show split character
    @property
    def split_char(self):
        return self.__split_chr
