from functools import partial
from .Container import AttributeDict
import ast
import re
import os

import warnings
def warning_on_one_line(message, category, filename, lineno, file=None, line=None):
    return "{0}:{1}: {2}: {3}\n".format(filename, lineno, category.__name__, message)
warnings.formatwarning = warning_on_one_line


class Type_Convertor(object):
    '''
        This helper class aims to parse the config string into
        the value of the corresponding type. Concerning security issue, we prevent to
        parse the harmful code by using eval(.). Instead, we constraint the parse capability
        by using ast.literal_eval(.), so feel free to use the default type converter. 
    '''
    def __init__(self, typ_split_chr:str = '@', filter_split_chr:str = ' | '):
        '''
        Constructor of type convertor. 

        Args:
            typ_split_chr (str, option): The character is used to split the declaration string in configer file.
                For example, 'a = 13@int' which means the argument 'a' is interger type data,
                and the '@' is the typ_split_chr. Default to `@`.

            filter_split_chr (str, option): The character is used to split the value string and 
                figure out the corresponding 'post-process' for the parsed value. For example, 
                'a = hello@str | upper', the upper post-processor will turn a into HELLO string.
                Default to ` | `.
        '''
        self.__split_chr = typ_split_chr
        self.__filter_chr = filter_split_chr
        self.__env_vars = AttributeDict(os.environ)

        # fundemental api-string supported in built-in 
        # i.e. "{{{}}}".format("'key':56")  ->  "{'key':56}", ast.literal_eval("{'key':56}") -> {'key':56}
        #      "{{{}}}".format("1, 2, 3")  ->  "{1, 2, 3}", ast.literal_eval("{1, 2, 3}") -> {1, 2, 3}
        #      so, dict and set apply the same api_str called curly_braces_str!
        curly_braces_str = "{{{}}}" ; lst_str = "[{}]" ; tuple_str = "({})" 
        # add security policy : we applied ast.literal_eval to eval str
        cnt_wrap = lambda val, api_str : ast.literal_eval(api_str.format(val))
       
        # create various converter by wrapping api_str into ast.literal_eval :
        curly_braces_cnvt = partial(cnt_wrap, api_str=curly_braces_str)
        tuple_cnvt = partial(cnt_wrap, api_str=tuple_str)
        lst_cnvt = partial(cnt_wrap, api_str=lst_str)

        # deal with bool(.) constructor feature, empty str regard as False
        bool_cnvt = lambda val: False if val == 'False' else bool(val)
        
        # basic datatype, build-in container, collection
        self.__default_cnvtor = {"str":str, "int":int, "float":float, "bool":bool_cnvt,
                                    "dict":curly_braces_cnvt, "set":curly_braces_cnvt, "tuple":tuple_cnvt, "list":lst_cnvt}
        self.__customized_cnvtor = {}
        self.__filter_cnvtor = {"upper":str.upper, "lower":str.lower, "strip":str.strip,
                                "str":str, "int":int, "float":float, "bool":bool}

    def convert(self, cfg_raw_str:str, tmp_cfg_node = None):
        '''
        Args:
            cfg_raw_str (str): The string which declare the arguments with the same syntax used in config file.
            
            tmp_cfg_node (AttributeDict): The container, which is used to intepolate the argument, store all arguments defined in config.
                Default to None.
        '''    
        
        def check_formation(formatted_str, raw_str):
            if '{' in formatted_str:
                raise RuntimeError(f"Format-string $'{raw_str}' failure, try to intepolate an undefined argument!")
        
        def pre_interpret_val_str(val_str):
            beg_tkn, end_tkn = "${", "}"
            # early return the value-string without python interpreter symbol "${...}"
            if beg_tkn not in val_str:
                return val_str
            
            parsed_str = ""
            idx = 0
            while idx < len(val_str):
                curr_tkn = val_str[ idx : idx+len(beg_tkn) ]
                
                if curr_tkn == beg_tkn:
                    beg_idx = idx+len(beg_tkn)

                    # offset present the length of python commend
                    offset_idx = val_str[beg_idx:].find(end_tkn)
                    if offset_idx == -1:
                        raise RuntimeError("Missing closed '}' for the python pharse.")
                    
                    end_idx = beg_idx + offset_idx

                    # keep '{' and '}' to form python format string by -1, +1 on both index
                    format_string = val_str[beg_idx-1 : end_idx+1]
                    
                    # https://stackoverflow.com/questions/15197673/using-pythons-eval-vs-ast-literal-eval
                    # Due to unsafty of eval(.), we only support argument intepolation by format-string
                    formatted_str = format_string.format(cfg=tmp_cfg_node, env=self.__env_vars)
                    
                    # chk parsed results & append string for further type conversion
                    check_formation(formatted_str, format_string)
                    parsed_str += formatted_str
                    
                    # point to next char (one position right-shift of '}')
                    idx = end_idx + 1

                else:  
                    parsed_str += val_str[idx]
                    idx += 1
            
            return parsed_str

        typ = ''
        token_lst = cfg_raw_str.split(self.__split_chr)
        # value string without declaring type
        if len(token_lst) == 1:
            raw_val_str = token_lst[0]
        else:
            raw_val_str, typ = token_lst

        # record filter method(s)
        token_lst = raw_val_str.split(self.__filter_chr)
        method_lst = []
        if len(token_lst) == 1:
            raw_val_str = token_lst[0]
        else:
            raw_val_str, *method_lst = token_lst

        # pre-interpret python syntax ${...python_stuff..} in config-string
        val_str = pre_interpret_val_str(raw_val_str)
        var_val = None
        if typ in self.__customized_cnvtor.keys():
            args = ast.literal_eval(val_str)
            # For init customized class, we provide args, kwargs or default init  
            if isinstance(args, dict):
                var_val = self.__customized_cnvtor[typ](**args)
            elif isinstance(args, list):
                var_val = self.__customized_cnvtor[typ](*args)
            else:  # invalid type of args is considered as default init  
                warnings.warn("You're initialized class '{0}' with default arguments!".format(typ))
                var_val = self.__customized_cnvtor[typ]()
        
        # bare string-value evaluator, instead of define '@type' at the end..
        #  responsible to eval 'None' placeholder and [], {}
        elif (val_str == 'None') or (not typ):  
            try: # all type can be parsed by plain string
                var_val = ast.literal_eval(val_str)
            except: # adding "'" quote-string to deal with string type value-string!! 
                var_val = ast.literal_eval(f"'{val_str}'")
            
        # type-validator : we use ast.literal_eval and it need to \
        else:  # strip '[', ']', '{', '}' notation before feeding into 'default' type-conveter
            stripped_val_str = re.sub(r"[\[\]\{\}\(\) ]", "", val_str)
            var_val = self.__default_cnvtor[typ](stripped_val_str)
        
        # post-processing 'value filtering'
        for method_name in method_lst:
            var_val = self.__filter_cnvtor[method_name](var_val)
        return var_val
    
    def regist_cnvtor(self, type_name:str = None, cnvt_func:callable = None):
        '''
        Regist the customized class. 
        
        Args:
            type_name (str): Name of registered function, namely the name of customized class. Default to None.
            
            cnvt_func (callable): The function for converting the string object into the customized class instance. Default to None.
        '''
        if not callable(cnvt_func):
            raise TypeError("The converter function is not callable.")
        
        if not (isinstance(type_name, str) and len(type_name) > 0):
            raise RuntimeError("The cnvt_name should be given")
        
        func_wrap = lambda *args, **kwargs : cnvt_func(*args, **kwargs)
        self.__customized_cnvtor[type_name] = func_wrap

    def regist_filter(self, filter_name:str = None, filter_func:callable = None):
        '''
            Regist the postprocessing function. 

            Args:
                type_name (str): Name of registered function, namely the name of customized class. Default to None.
                
                cnvt_func (callable): The function for converting the string object into the customized class instance. Default to None.
        '''
        if not callable(filter_func):
            raise TypeError("The converter function is not callable.")
        
        if not (isinstance(filter_name, str) and len(filter_name) > 0):
            raise RuntimeError("The cnvt_name should be given")
        
        func_wrap = lambda var_val : filter_func(var_val)
        self.__filter_cnvtor[filter_name] = func_wrap