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
    def __init__(self, typ_split_chr:str = '@', lambda_split_chr:str = ' | '):
        '''
        Constructor of type convertor. 

        Args:
            typ_split_chr (str, option): The character is used to split the declaration string in configer file.
                For example, 'a = 13@int' which means the argument 'a' is interger type data,
                and the '@' is the typ_split_chr. Default to `@`.

            lambda_split_chr (str, option): The character is used to split the value string and 
                figure out the corresponding 'post-process' for the parsed value. For example, 
                'a = hello@str | upper', the upper post-processor will turn a into HELLO string.
                Default to ` | `.
        '''
        # viewable for multiline parser
        self._split_chr = typ_split_chr
        self.__lambda_chr = lambda_split_chr
        # os.environ in win is converted to uppercase, while linux is case sensitive
        #   to better interpolate in config file, we force global env to lowercase!
        self.__env_vars =  AttributeDict( init_dict={ k.lower(): v for k, v in os.environ.items() } )
        
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
        self.__lambda_cnvtor = {"upper":str.upper, "lower":str.lower, "strip":str.strip,
                                "str":str, "int":int, "float":float, "bool":bool}

    def convert(self, cfg_raw_str:str, tmp_cfg_node = None):
        '''
        Args:
            cfg_raw_str (str): The string which declare the arguments with the same syntax used in config file.
            
            tmp_cfg_node (AttributeDict): The container, which is used to intepolate the argument, store all arguments defined in config.
                Default to None.
        '''    
        def pre_interpret_val_str(val_str):
            beg_tkn, end_tkn = "${", "}"

            # early return the value-string without python interpreter symbol "${...}"
            #   don't use walrus operator, make it competible (< python 3.7)
            idx = val_str.find(beg_tkn)
            if idx == -1:
                return val_str
            
            # keep '{'  to form python format string by -1 on begin index
            parsed_str, unparsed_str = val_str[:idx], val_str[idx+len(beg_tkn)-1:]
            # recursive calling for 2 case : 
            #     1. "${..." + "...}_${...}", return  "${..." + "...}_ABC"
            #     2. "${..." + "...${...}...}" return "${..." + "...ABC...}"
            unparsed_str = pre_interpret_val_str(unparsed_str)
            
            end_idx = unparsed_str.find(end_tkn)
            if end_idx == -1:
                raise RuntimeError("Missing closed '}' for the python pharse.")
            
            # keep '}' to form python format string by +1 on ending index
            format_string, rest_str = unparsed_str[:end_idx+1], unparsed_str[end_idx+1:]

            # pre-set default value in global env variable
            if '{env.' in format_string:
                var_name = format_string[len('{env.'):-1]
                # we respect default value in get method in dict
                self.__env_vars[var_name] = self.__env_vars.get(var_name, None)
                
            try:
                # https://stackoverflow.com/questions/15197673/using-pythons-eval-vs-ast-literal-eval
                # Due to unsafty of eval(.), we only support argument intepolation by format-string
                formatted_str = format_string.format(cfg=tmp_cfg_node, env=self.__env_vars)
            except AttributeError:
                # don't use f-string, make it competible (< python 3.7)
                raise RuntimeError("Format-string $'{0}' failure, try to intepolate an undefined argument!".format(format_string))
            
            return parsed_str + formatted_str + rest_str

        # record lambda method(s)
        method_lst = []
        token_lst = cfg_raw_str.split(self.__lambda_chr)
        if len(token_lst) == 1:
            raw_val_str = token_lst[0]
        else:
            raw_val_str, *method_lst = token_lst

        # value string without declaring type
        token_lst = raw_val_str.split(self._split_chr)
        typ = ''
        if len(token_lst) == 1:
            raw_val_str = token_lst[0]
        else:
            raw_val_str, typ = token_lst
        
        # pre-interpret argument interpolation ${...} in config-string
        # due to saft policy, we do not naturally permit python code interpretation!
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
                warnings.warn("Invalid type of args '{0}' is considered as default init, you're initialized class '{1}' with default arguments!".format(args, typ))
                var_val = self.__customized_cnvtor[typ]()
        
        # bare string-value evaluator, instead of define '@type' at the end..
        #  responsible to eval 'None' placeholder and [], {}
        elif (val_str == 'None') or (not typ):  
            try: # all type can be parsed by plain string
                var_val = ast.literal_eval(val_str)
            except: # Patch : adding "'" quote-string to deal with string type value-string!! 
                var_val = ast.literal_eval(f"'{val_str}'")
            
        # type-validator : we use ast.literal_eval and it need to \
        else:  # strip '[', ']', '{', '}' notation before feeding into 'default' type-conveter
            stripped_val_str = re.sub(r"[\[\]\{\}\(\) ]", "", val_str)
            var_val = self.__default_cnvtor[typ](stripped_val_str)
            
        # post-processing 'lambda transform value'
        # pay attention about security issue while registering 'eval' lambda!
        #   it prohibited in most of case, you should not do it...
        for method_name in method_lst:
            try:
                var_val = self.__lambda_cnvtor[method_name](var_val)
            except KeyError:
                kerr_msg = "The lambda name '{}' haven't been registered yet!".format(method_name)
                raise KeyError(kerr_msg) from None
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

    def regist_lambda(self, lambda_name:str, lambda_func:callable):
        '''
            Regist the postprocessing function. 

            Args:
                lambda_name (str): Name of registered function, namely the name of customized lambda function. 
                
                lambda_func (callable): convert the object by lambda function. 
        '''
        if not callable(lambda_func):
            raise TypeError("The converter function is not callable.")
        
        if not (isinstance(lambda_name, str) and len(lambda_name) > 0):
            raise RuntimeError("The cnvt_name should be given")
        
        func_wrap = lambda var_val : lambda_func(var_val)
        self.__lambda_cnvtor[lambda_name] = func_wrap