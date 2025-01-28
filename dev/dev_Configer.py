import errno
import os
import sys
from copy import deepcopy
from pathlib import Path

import warnings
def warning_on_one_line(message, category, filename, lineno, file=None, line=None):
    return "{0}:{1}: {2}: {3}\n".format(filename, lineno, category.__name__, message)
warnings.formatwarning = warning_on_one_line

from .dev_Container import AttributeDict, Flag
#from easy_configer.utils.Container import AttributeDict, Flag

from .dev_Type_Convertor import Type_Convertor
from .dev_IO_Converter import IO_Converter


class Parser(object):
    def __init__(self, cmd_args):
        self.__cmd_args = cmd_args
        self.__split_chr = " = "
        self.cnt_ptr = AttributeDict()
        self.__typ_cnvt = Type_Convertor()

    #  utils of config parser
    def _preproc_cfgstr(self, cfg_str:str) -> str:
        ''' preprocess the config string with strip the empty line and comments. '''
        # eliminate the line full of white-space without any text
        cfg_str = cfg_str.strip() 
        # skip empty line and comment line 
        if len(cfg_str) == 0 or cfg_str[0] == '#': 
            return ''
        # strip inline comment's content with strip extra-whitespace
        return cfg_str.split('#')[0].strip()

    def _get_sec(self, cfg_str:str) -> str:
        ''' get section name of config string. '''
        if '[' != cfg_str[0]:
            return ''
        # more robust with Indented section
        beg, end = cfg_str.find('['), cfg_str.rfind(']')
        if end == -1:
            raise RuntimeError("Configuration Error : Invalid section notation, missing ']' at end of line")
        sec_key_str = cfg_str[beg+1 : end].strip()
        return sec_key_str
    
    def _idx_sec_parent_by_dot(self, sec_keys_str:str, allow_init:bool = False):  
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
            return self.cnt_ptr, sec_keys_str

        ## Support toml like 'hierachical' format!!
        #  dynamically search the hierachical section begin from the 'next layer' of self.cnt_ptr (container pointer)
        idx_sec = self.cnt_ptr
        
        #  omit the last search string to keep the final index point to the "parent" node, 
        #  since the child node will be init as dict!
        for idx, sec in enumerate(sec_name_lst[:-1]):
            if sec not in idx_sec:
                if not allow_init:
                    raise RuntimeError("The parent node '{0}' is not defined yet, " \
                                        "it's invalid for directly made the child node '{1}'".format(sec, sec_name_lst[idx+1]))
                idx_sec[sec] = AttributeDict() 
            idx_sec = idx_sec[sec]

        return idx_sec, sec_name_lst[-1]

    def _get_declr_dict(self, cfg_str:str) -> dict : 
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
            var_val = self.__typ_cnvt.convert(val_str, self.cnt_ptr)
        except:
            raise RuntimeError("Configuration Error : Invalid config string, '{0}'.".format(cfg_str))

        return { var_name : var_val }
    
    def args_from_cmd(self) -> None:   
        '''
            Update the arguments by commend line input string.
            Note that this method allow overwrite the pre-define config natively (with silent mode).
            ( Because commentline inputs are explicitly given by user, we don't need to warn that )
        '''
        # ' = ' -> '=', eliminate white space
        cmd_sp_chr = self.__split_chr.strip()

        # filter out all non-argument
        cmd_arg_lst = [ arg for arg in sys.argv \
                            if cmd_sp_chr in arg]
        
        # print out helper document string
        if "-h" in cmd_arg_lst:
            cmd_arg_lst.remove("-h")
            #print(self.__help_info)

        sec_ptr, sec_key = None, None 
        for item in cmd_arg_lst:
            itm_lst = [ itm for itm in item.split(cmd_sp_chr) if itm != '']
            if len(itm_lst) != 2:
                raise RuntimeError("Invalid commendline input : the split char '{}' should only present once and the value should be given!".format(cmd_sp_chr))
            
            sec_keys_str, val_str = itm_lst
            sec_ptr, sec_key = self._idx_sec_parent_by_dot(sec_keys_str, allow_init=True)
            
            # For the section already exists, 
            # Prevent client argument easily overwrite the section..
            if sec_key in sec_ptr:
                # ? overwrite section by a value is sick!
                if isinstance(sec_ptr[sec_key], AttributeDict): 
                    raise RuntimeError("Client argument {} attempt to overwrite pre-defined section.".format(sec_keys_str))
                
            sec_ptr[sec_key] = self.__typ_cnvt.convert(val_str)

        if len(cmd_arg_lst) == 0:
            warnings.warn('Accept no client argument from commend line.')
        
    # core function of config parser
    def parsing_config(self, raw_cfg_text:str, allow_overwrite:bool) -> None:
        '''
            Core function to parse the raw config string line-by-line. It'll dispatch each line of config string 
            to the corresponding subroutine. Basically, subroutines is categorized into 3 types in order :
            1. _preproc_cfgstr : to preprocess the config string by stripping empty line and comments.
            2. _get_sec : get the section name, a kind of id to indicate the nested dict of hierachical config.
            3. _get_declr_dict : parse the value string to get the value dictionary.

            Args:
                raw_cfg_text (str): The raw config strings. It could event include comment.
                allow_overwrite (bool): A flag allow overwrite config from the other source,
                    such as the other .ini config file, config string. Default to False.
            
            Return:
                None. After config parsing, we access each argument by using this instance.
                So we don't return anything.
        '''
        def chk_args_exists(val_dict:dict, container:dict):
            ''' checking argument already exists in the value dict. '''
            key = list(val_dict.keys())[0]
            if key in container:
                raise RuntimeError("Re-define Error : argument '{0}' is already defined.".format(key))
            
        # initially, all arguments placed in first level
        container = self.cnt_ptr
        for lin in raw_cfg_text.splitlines():
            # strip empty space and 'skip' empty line in cfgstr
            cfg_str = self._preproc_cfgstr(lin)
            if not cfg_str:
                continue

            # get the section key of config string (if there exists)
            sec_keys_str = self._get_sec(cfg_str)
            if sec_keys_str:
                idx_sec_parent, idx_sec_key = self._idx_sec_parent_by_dot(sec_keys_str)
                # if sec hasn't defined yet, make a new container
                if idx_sec_key not in idx_sec_parent.keys():
                    idx_sec_parent[idx_sec_key] = AttributeDict()
                # point to the container the following arguments belong to..
                container = idx_sec_parent[idx_sec_key]
                
            # parse variable assignment string
            else:
                # parse the value string into dict
                if cfg_str[0] == '>':
                    # import other .ini config as AttributeDict
                    sub_cfg_path = cfg_str.split('>')[-1].strip()
                    val_dict = Configer.cfg_from_ini(sub_cfg_path, allow_overwrite, self.__cmd_args)
                else:
                    # normal value string, return pure dict
                    val_dict = self._get_declr_dict(cfg_str)
                
                (not allow_overwrite) and chk_args_exists(val_dict, container)
                container.update(val_dict)
                    
        # Update the namespace value via commend-line input 
        if self.__cmd_args:
            self.args_from_cmd()

        return self.cnt_ptr
    

class Configer(object):
    '''
        The core module of easy_configer to implement the user configuration system.
    '''
    help_info = "Description : \n"
    cfg_cnvt = IO_Converter()

    ## Main interface for configuration :         
    # Support string config in cell-based intereactive enviroment
    @staticmethod
    def cfg_from_cli(allow_overwrite_sec:bool=False):
        parser = Parser(cmd_args=True)
        parser.args_from_cmd()

    @staticmethod
    def cfg_from_str(raw_cfg_text:str, allow_overwrite:bool=False, cmd_args=False) -> None:
        ''' 
            Building config from the given config string.

            Args: 
                raw_cfg_text (str): The string which declare the arguments with the same syntax used in config file.
                allow_overwrite (bool, optional): A flag allow overwrite config from the other source,
                    such as the other .ini config file, config string. Default to False.
        '''
        parser = Parser(cmd_args)
        return parser.parsing_config(raw_cfg_text, allow_overwrite)
    
    # Load .ini config from the given path
    @staticmethod
    def cfg_from_ini(cfg_path:str, allow_overwrite:bool=False, cmd_args=False) -> None:
        '''
            Building config from the given .ini config file.

            Args:
                cfg_path (str): The path which locate the '*.ini' config file.
                allow_overwrite (bool, optional): A flag allow overwrite config from the other source,
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
        except PermissionError as per_err:
            print(per_err) ; raise
        except Exception as ex:
            print(ex) ; raise
        
        return Configer.cfg_from_str(raw_cfg_text, allow_overwrite, cmd_args)

    @staticmethod
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
        Type_Convertor.regist_cnvtor(type_name, cnvt_func)
        
    @staticmethod
    def regist_filter(filter_name:str = None, filter_func:callable = None):
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
        Type_Convertor.regist_filter(filter_name, filter_func)
    