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
from .utils.Container import AttributeDict, Flag
from .IO_Converter import IO_Converter

from typing import List

class Configer(object):
    '''
        The core module of easy_configer to implement the user configuration system.
    '''
    def __init__(self, description:str = "", cmd_args:bool = False, split_chr:str = " = ") -> None:
        '''
            Constructor of Configer.

            Args:
                description (str, optional): A customized helper information which describe the role of config file. Defaults to ''.
                cmd_args (bool, optional): A flag to indicate reading argument from commendline and override the default config. Defaults to False.
                split_chr (str, optional): A char-string used to format the config syntax. Defaults to ' = '.
                    For example, 'a*13@int' which means the argument 'a' contain interger value 13,
                    and the '*' is the split_chr.
                    Note that better not to change this char-string to prevent the symbol conflict.

            Returns:
                None. Don't accept anything return from constructor.
        '''
        self.__help_info = "Description : \n" + description
        self.__typ_cnvt = Type_Convertor()
        self.__cfg_cnvt = IO_Converter()
        self.__split_chr = split_chr
        self.__flag = Flag().FLAGS
        self.__cmd_args = cmd_args

    ## Main interface for configuration : 
    # Support commendline config
    def cfg_from_cli(self) -> None:
        ''' 
            Building config from the commendline input and only apply the arguments from commend-line.
            ( only recommend for very lightweight config ) 
        '''
        if not self.__cmd_args:
            warnings.warn("'cfg_from_cli' is called, the settings 'cmd_args=False' will be ignored!")
        self.args_from_cmd()
            
    # Support string config in cell-based intereactive enviroment
    def cfg_from_str(self, raw_cfg_text:str, allow_override:bool=False) -> None:
        ''' 
            Building config from the given config string.

            Args: 
                raw_cfg_text (str): The string which declare the arguments with the same syntax used in config file.
                allow_override (bool, optional): A flag allow override config from the other source,
                    such as the other .ini config file, config string. Default to False.
        '''
        self.__cfg_parser(raw_cfg_text, allow_override)
        # build the flag object 
        self.__flag.__dict__ = self.__dict__
    
    # Load .ini config from the given path
    def cfg_from_ini(self, cfg_path:str, allow_override:bool=False) -> None:
        '''
            Building config from the given .ini config file.

            Args:
                cfg_path (str): The path which locate the '*.ini' config file.
                allow_override (bool, optional): A flag allow override config from the other source,
                    such as the other .ini config file, config string. Default to False.
        '''
        def chk_src(cfg_path):
            ''' checking config file with the valid suffix and can be readed. '''
            if not cfg_path.exists():
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), str(cfg_path))
            if not cfg_path.suffix == ".ini":
                raise ValueError("The file extension should be 'ini', instead of '{0}'".format(cfg_path.suffix))
        
        # take from : https://stackoverflow.com/questions/16480495/read-a-file-with-line-continuation-characters-in-python
        def continuation_lines(fin):
            ''' support the multi-line declaration in config file. '''
            for line in fin:
                line = line.rstrip('\n')
                while line.endswith('\\'):
                    line = line[:-1] + next(fin).rstrip('\n')
                yield line

        try:
            # check config path validation
            cfg_path = Path(cfg_path)
            chk_src(cfg_path)

            with cfg_path.open('r') as cfg_ptr: 
                raw_cfg_text = "\n".join([ line for line in continuation_lines(cfg_ptr) ])
            
        except FileNotFoundError as fnf_err:
            print(fnf_err) ; raise
        except ValueError as val_err:
            print(val_err) ; raise
        except PermissionError as per_err:
            print(per_err) ; raise
        except Exception as ex:
            print(ex) ; raise
        
        self.__cfg_parser(raw_cfg_text, allow_override)
        # build the flag object 
        self.__flag.__dict__ = self.__dict__
    
    ## Core implementation of config parser : 
    #  utils of config parser
    def __preproc_cfgstr(self, cfg_str:str) -> str:
        ''' preprocess the config string with strip the empty line and comments. '''
        # eliminate the line full of white-space without any text
        cfg_str = cfg_str.strip() 
        # skip empty line and comment line 
        if len(cfg_str) == 0 or cfg_str[0] == '#': 
            return ''
        # strip inline comment's content with strip extra-whitespace
        return cfg_str.split('#')[0].strip()

    def __get_sec(self, cfg_str:str) -> str:
        ''' get section name of config string. '''
        if '[' != cfg_str[0]:
            return ''
        # more robust with Indented section
        beg, end = cfg_str.find('['), cfg_str.rfind(']')
        if end == -1:
            raise RuntimeError("Configuration Error : Invalid section notation, missing ']' at end of line")
        sec_key_str = cfg_str[beg+1 : end].strip()
        return sec_key_str
    
    def __idx_sec_by_dot(self, sec_keys_str:str, allow_init:bool = False):  
        '''
            Core function to manage the hierachical config. 
            Store args is simple, just add it in dict. But dynamically search argument in specific section is non-trivial!
            Therefore, i wrote this function to deal with searching and return the "pointer" point to the section.
            It's sync with self.__dict__, so use it wiselly & carefully!!

            Args:
                sec_keys_str (str): A qurey string for indexing the hierachical section.
                allow_init (bool): A flag to indicate initializing the section without declared it before.
                    This flag should be turn on iff perform self.args_from_cmd(.). Default to False.
            
            Return:
                [dict, str] : dict is the config section, str is section name.
        '''
        sec_name_lst = sec_keys_str.split('.')
        # Before easy_configer 1.3.4 ver, all section is builded upon this level
        if len(sec_name_lst) == 1:
            return self.__dict__, sec_keys_str
            
        root_key = sec_name_lst.pop(0)
        if root_key not in self.__dict__:
            if not allow_init:
                raise RuntimeError("The parent node '{0}' is not defined yet, " \
                                    "it's invalid for directly made the child node '{1}'".format(root_key, sec_name_lst[0]))
            self.__dict__[root_key] = AttributeDict() 
            
        ## Support toml like 'hierachical' format!!
        #  dynamically search the hierachical section begin from the 'next layer' of self.__dict__
        idx_sec = self.__dict__[root_key]
        
        #  keep the index point to the node "parent", since the child node will be init as dict!
        for idx, sec in enumerate(sec_name_lst[:-1]):
            # AttributeDict.get(.) will not trigger "defaultdict behavior"
            tmp = idx_sec.get(sec, '__UNDEFINE_VAL')
            if tmp == '__UNDEFINE_VAL':
                if not allow_init:
                    raise RuntimeError("The parent node '{0}' is not defined yet, " \
                                        "it's invalid for directly made the child node '{1}'".format(sec, sec_name_lst[idx+1]))
                idx_sec[sec] = AttributeDict() 
            idx_sec = idx_sec[sec]

        return idx_sec, sec_name_lst[-1]

    def __get_declr_dict(self, cfg_str:str) -> dict : 
        '''
            Parse the value string and return the value dict to main routine for updating the config. 
            
            Args:
                cfg_str (str): A value string for declaring the argument name and its value.
                
            Return:
                dict: A value dictionary, the key is variable name and the value is corresponding parsed value.
        '''
        if self.__split_chr not in cfg_str:
            raise RuntimeError("Configuration Error : Split character '{0}'" \
                                " not found in '{1}'".format(self.__split_chr, cfg_str))
        
        try:
            var_name, val_str = cfg_str.split(self.__split_chr)
            # Due to security issue, we 'DO NOT' support '${...}' for single-line python code execution!!
            # '${...}' will only strictly used to access the configer argument..
            var_val = self.__typ_cnvt.convert(val_str, self)
        except:
            raise RuntimeError("Configuration Error : Invalid config string, '{0}'.".format(cfg_str))

        return { var_name : var_val }

    # core function of config parser
    def __cfg_parser(self, raw_cfg_text:str, allow_override:bool) -> None:
        '''
            Core function to parse the raw config string line-by-line. It'll dispatch each line of config string 
            to the corresponding subroutine. Basically, subroutines is categorized into 3 types in order :
            1. __preproc_cfgstr : to preprocess the config string by stripping empty line and comments.
            2. __get_sec : get the section name, a kind of id to indicate the nested dict of hierachical config.
            3. __get_declr_dict : parse the value string to get the value dictionary.

            Args:
                raw_cfg_text (str): The raw config strings. It could event include comment.
                allow_override (bool): A flag allow override config from the other source,
                    such as the other .ini config file, config string. Default to False.
            
            Return:
                None. After config parsing, we access each argument by using this instance.
                So we don't return anything.
        '''
        def parse_sub_config(sub_cfg_path:str):
            '''
                Support subconfig (nested config) in the config file.
            
                Args:
                    sub_cfg_path (str): The path of interpolated config. The sub-config path 
                        is parsed from the .ini file with split '>' symbol.
            '''
            sub_cfg = Configer(cmd_args=False)
            sub_cfg.cfg_from_ini(sub_cfg_path)
            return self.__cfg_cnvt.cnvt_cfg_to(sub_cfg, 'dict', return_attr_dict=True)

        def chk_args_exists(val_dict:dict, container:dict):
            ''' checking argument already exists in the value dict. '''
            key = list(val_dict.keys())[0]
            if key in container:
                raise RuntimeError("Re-define Error : duplicated argument '{0}' is defined.".format(key))
            
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
                    raise RuntimeError("Re-define Error : config section '{0}' is duplicated, section can not be overrided.".format(sec_keys_str))
                idx_sec[idx_sec_key] = AttributeDict()
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
                
                container = None
                # assign the val_dict into the corresponding section!
                if cur_sec_keys != '':
                    idx_sec, idx_sec_key = self.__idx_sec_by_dot(cur_sec_keys)
                    container = idx_sec[idx_sec_key]
                # assign the val_dict as 'flatten' arguments 
                else: # Note that flatten args IS NOT AttributeDict!
                    container = self.__dict__
                
                (not allow_override) and chk_args_exists(val_dict, container)
                container.update(val_dict)
                    
        # Update the namespace value via commend-line input 
        if self.__cmd_args:
            self.args_from_cmd()

    def args_from_cmd(self) -> None:   
        '''
            Update the arguments by commend line input string.
            Note that this method allow override the pre-define config natively (with silent mode).
            ( Because commentline inputs are explicitly given by user, we don't need to warn that )
        '''
        # remove file name from args
        cmd_arg_lst = sys.argv[1:]
        
        # print out helper document string
        if "-h" in cmd_arg_lst:
            cmd_arg_lst.remove("-h")
            print(self.__help_info)

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
        ''' 
        Support merge two config 'with override' the left-hand side config. 
        For example. cfg_a = cfg_a | cfg_b, cfg_a will be overrided by cfg_b.

        Args:
            cfg (AttributeDict): A container used to store the argument. it inherit from dict and the given input could be a nested dict.
        '''
        cp_cfg = deepcopy(self)
        cp_cfg.merge_conf(cfg, override=True)
        return cp_cfg

    #   concate operator 
    def __add__(self, cfg):
        ''' 
        Support merge two config 'without override' the any config. 
        This method call self.concate_cfg(.) underhood.

        Args:
            cfg (AttributeDict): A container used to store the argument. it inherit from dict and the given input could be a nested dict.
        
        Raise: 
            RuntimeError with re-define argument.
        '''
        return self.concate_cfg(cfg)

    # concate just means merge2conf "without" any override!!
    def concate_cfg(self, cfg):
        ''' 
        Merge two config 'without override' the any config. 
        
        Args:
            cfg (AttributeDict): A container used to store the argument. it inherit from dict and the given input could be a nested dict.
        
        Raise: 
            RuntimeError with re-define argument.

        Return:
            Configer.
        '''
        cp_cfg = deepcopy(self)
        cp_cfg.merge_conf(cfg, override=False)
        return cp_cfg
        
    #   merge conf suppose 2 config have overlap section, otherwise use 'concate' method!
    def merge_conf(self, cfg, override=True):
        ''' 
        Merge two config 'with override' the config. The config will be overrided
            by the given config cfg.

        Args:
            cfg (AttributeDict): A container used to store the argument. it inherit from dict and the given input could be a nested dict.  
            override (bool): A flag to indicate overriding value by the given config cfg. Default to True.

        Return:
            None. This is inplace operation.
        '''
        def hier_merge(sf_dict, cfg_dict):
            ''' Merge the nested dict config recursively. '''
            for sec_key, sec_val in cfg_dict.items():
                # same section exists
                if sec_key in sf_dict.keys():
                    if not override:
                        raise RuntimeError("Re-define Error : Key '{0}' in input config already exists in merged config!!".format(sec_key))
                    
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

    def __shadow_private_args(self):
        ''' 
        Remove the argument with '_' perfix. This method is used to display the namespace 
        which record all of the declared arguments. For argument belong in nested dict, it
        will call __str__ recursively.
        '''
        return [ str(key) for key in self.__dict__.keys() if key[0] != '_' ] 

    def __str__(self):
        ''' Present all 'non-private' arguments defined in config. '''
        key_str = self.__shadow_private_args()
        return "Namespace : \n" + ", ".join(key_str)
    # override default __repr__ to view configer in debugger
    __repr__ = __str__

    ## public interface for iterate the entire config
    def __iter__(self):
        ''' Return iterator for Configer. Because Configer itself isn't dict. '''
        tmp_dct = {}
        for key in self.__shadow_private_args():
            tmp_dct[key] = self.__dict__[key]
        return iter(tmp_dct)
    
    ## standard interface for dict-access for flatten argument (since Configer IS NOT AttributeDict)
    def __getitem__(self, key):
        ''' Support getitem for Configer. Because Configer itself isn't dict. '''
        return self.__dict__[key]

    def __setitem__(self, key, value):
        ''' Support setitem for Configer. Because Configer itself isn't dict. '''
        self.__dict__[key] = value

    def get(self, key, default_value=None):
        ''' Support get for Configer. Because Configer itself isn't dict. '''
        if key not in self.__dict__:
            return default_value
        return self.__dict__[key]
    
    ## Miscellnous functionality : 
    # return an absl style flag to store all of the args.
    def get_cfg_flag(self):
        ''' Return the FLAG object which 'sync' the config. '''
        return self.__flag

    def get_doc_str(self):
        ''' Return the helper information string. '''
        return self.__help_info

    def regist_cnvtor(self, type_name:str = None, cnvt_func:callable = None):
        ''' 
        Declare the user customized class. The registered type (class) can be used 
        to declare the argument in the config file.

        Args:
            type_name (str): type name used in config file. i.e. registered as 'dummy', 
                then declare a argument with such type will be `var = {'arg1':42}@dummy`.
            
            cnvt_func (callable): typically it's the constructor of your customized class.
                So, you can just directly feed the customized class as this arguemnt.
        
        Return:
            None. This registered method doesn't return any flag.
        '''
        self.__typ_cnvt.regist_cnvtor(type_name, cnvt_func)

    def regist_filter(self, filter_name:str = None, filter_func:callable = None):
        ''' 
        Declare the user customized function for post-processor. The registered converter can be used 
        to declare in the config file.

        Args:
            filter_name (str): filter name used in config file. i.e. registered as 'dummy', 
                then declare a post-processor will be `var = 42 | dummy`.
            
            filter_func (callable): typically it's the function for post-processing the argument.
                For example, `lambda x : str(x)` is a simple string type convresion.
        
        Return:
            None. This registered method doesn't return any flag.
        '''
        self.__typ_cnvt.regist_filter(filter_name, filter_func)
    
    # show split character
    @property
    def split_char(self):
        ''' Show the split char used in config file. '''
        return self.__split_chr
