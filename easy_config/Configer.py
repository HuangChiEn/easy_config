import errno
import os
from pathlib import Path
import sys
from dataclasses import dataclass

from .utils.Type_Convertor import Type_Convertor
from .utils.Flag import Flag

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
        self.doc_str = "Description : \n" + description
        self.__typ_cnvt = Type_Convertor()
        self.__split_chr = split_chr
        self.__cmd_args = cmd_args
        self.__cmd_arg_lst = sys.argv[1:]
        self.__flag = Flag().FLAGS
            
        # print out helper document string
        if cmd_args and "-h" in self.__cmd_arg_lst:
            self.__cmd_arg_lst.remove("-h")
            print(self.doc_str)
            
    # The cell-base Intereactive Enviroment Support function
    def cfg_from_str(self, raw_cfg_text:str):
        ''' 
            raw_cfg_text :
                The string which declare the arguments with the same syntax used in config file. 
        '''
        self.__cfg_parser(raw_cfg_text)
        # build the flag object 
        self.__flag.__dict__ = self.__dict__
         
    def cfg_from_ini(self, cfg_path:str):
        '''
            cfg_path :
                The path which locate the '*.ini' config file.
        '''
        def chk_src(cfg_path):
            if not cfg_path.exists():
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), str(cfg_path))
            if not cfg_path.suffix == ".ini":
                raise ValueError("The file extension should be 'ini', instead of '{}'".format(cfg_path.suffix))
            
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

    # return an absl style flag to store all of the args.
    def get_cfg_flag(self):
        return self.__flag

    # utils of config parser
    def __preproc_cfgstr(self, cfg_str:str) -> str:
        # eliminate the line full of white-space without any text
        cfg_str = cfg_str.strip() 
        # skip empty line and comment line 
        if len(cfg_str) == 0 or cfg_str[0] == '#': 
            return ''
        # strip inline comment's content with strip extra-whitespace
        return cfg_str.split('#')[0].strip()

    def __get_sec(self, cfg_str:str) -> str:
        if '[' not in cfg_str:
            return ''
        # more robust with Indented section
        beg, end = cfg_str.find('['), cfg_str.rfind(']')
        if end == -1:
            raise RuntimeError("Configuration Error : Invalid section notation, missing ']' at end of line")
        sec_key = cfg_str[beg+1 : end].strip()
        return sec_key

    def __get_declr_dict(self, cfg_str:str) -> dict : 
        if self.__split_chr not in cfg_str:
            raise RuntimeError(f"Configuration Error : Split character '{self.__split_chr}' not found in '{cfg_str}'")
        
        try:
            var_name, val_str = cfg_str.split(self.__split_chr)
            # support '$' args interpolation
            var_val = self.__dict__[ val_str[1:] ]  if val_str[0] == '$' \
                        else self.__typ_cnvt.convert(val_str)
        except:
            raise RuntimeError(f"Configuration Error : Invalid config string ' {cfg_str}' ")

        return { var_name : var_val }

    def __cfg_parser(self, raw_cfg_text:str):
        '''
            raw_cfg_text :
                The string which declare the arguments with the same syntax used in config file.
        '''
        cur_sec_key = ''
        for lin in raw_cfg_text.splitlines():
            # strip empty space and 'skip' empty line in cfgstr
            cfg_str = self.__preproc_cfgstr(lin)
            if not cfg_str:
                continue

            # get the section key of config string (if there exists)
            sec_key = self.__get_sec(cfg_str)
            if sec_key:
                self.__dict__[sec_key] = {}
                cur_sec_key = sec_key
            # parse variable assignment string
            else:
                val_dict = self.__get_declr_dict(cfg_str)
                if cur_sec_key != '':
                    self.__dict__[cur_sec_key].update( val_dict )
                else:
                    self.__dict__.update( val_dict )

        # update args from commandline input        
        if self.__cmd_args:
            self.__args_from_cmd()
        
    # Update the namespace value via commend-line input 
    def __args_from_cmd(self):
        '''
            Update the arguments by commend line input string
        '''

        def is_long_flag(flag_str):
            prefix = flag_str[0:2]
            return True if prefix == "--" else False
            
        for idx, item in enumerate(self.__cmd_arg_lst):
            if idx % 2 == 0:  # argument flag 
                if is_long_flag(item):
                    flag = item[2:]
                    flag_lst = flag.split('-')
                    sec_key, arg = flag_lst[0], flag_lst[1]
                else:
                    arg = item[1:]
                    sec_key = ""
                    
            else:     # argument value 
                val = item
                if sec_key == "":
                    self.__dict__[arg] = val
                else:
                    self.__dict__[sec_key][arg] = val

    # Display the namespace which record all of the declared arguments
    #   for the inner-node structure, iter-call __str__ wrapper !!
    def __str__(self):
        key_str = [ str(key) for key in self.__dict__.keys() if key[0] != '_' ] 
        return "Namespace : \n" + ", ".join(key_str)

    # For the declare the instance of user customized class 
    def regist_cnvtor(self, *args:list, **kwargs:dict):
        self.__typ_cnvt.regist_cnvtor(*args, **kwargs)
    
    # show split character
    @property
    def split_char(self):
        return self.__split_chr
