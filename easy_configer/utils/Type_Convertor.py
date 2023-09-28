from functools import partial
import ast
import re

import warnings
def warning_on_one_line(message, category, filename, lineno, file=None, line=None):
    return "{}:{}: {}: {}\n".format(filename, lineno, category.__name__, message)
warnings.formatwarning = warning_on_one_line


class Type_Convertor(object):
    '''
        As the name implies, this helper class of Configer will convert the raw string of config file
        into variable of the corresponding type.
        
        Now, i have update the security policy to prevent loading the harmful code to your system ~
        feel free to use the default type converter. 

        However, we still apply eval in regist_cnvtor, plz be careful about register the customized classes ~
    '''
    def __init__(self, typ_split_chr:str = '@'):
        '''
            typ_split_chr (option) :
                The character make use to split the declaration string in configer file.
                For example, 'a*13@int' which means the argument 'a' is interger type data,
                and the '@' is the typ_split_chr.
        '''
        self.__split_chr = typ_split_chr

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

    def convert(self, cfg_raw_str:str):
        '''
            cfg_raw_str :
                The string which declare the arguments with the same syntax used in config file.
        '''    
        # force to add split character at the end of parsed string
        cfg_raw_str = cfg_raw_str + self.__split_chr if (not self.__split_chr in cfg_raw_str) else cfg_raw_str
        try:
            val_str, typ = cfg_raw_str.split(self.__split_chr)
        except:
            raise RuntimeError
        
        if typ in self.__customized_cnvtor.keys():
            args = ast.literal_eval(val_str)
            # For init customized class, we provide args, kwargs or default init  
            if isinstance(args, dict):
                return self.__customized_cnvtor[typ](**args)
            elif isinstance(args, list):
                return self.__customized_cnvtor[typ](*args)
            else:  # invalid type of args is considered as default init  
                warnings.warn(f"You're initialized class '{typ}' with default arguments!")
                return self.__customized_cnvtor[typ]()
        
        # support 'None' placeholder and [], {} eval, instead of define '@type'
        elif (val_str == 'None') or (not typ):  
            return ast.literal_eval(val_str)
        
        # type-validator : we use ast.literal_eval and it need to \
        else:  # strip '[', ']', '{', '}' notation before feeding into 'default' type-conveter
            stripped_val_str = re.sub(r"[\[\]\{\}]", "", val_str)
        return self.__default_cnvtor[typ](stripped_val_str)
    
    def regist_cnvtor(self, type_name:str = None, cnvt_func:callable = None):
        '''
            type_name :
                Name of registered function, namely the name of customized class.
            
            cnvt_func :
                The function for converting the string object into the customized class instance.
        '''
        assert callable(cnvt_func), "The converter function should be callable."
        assert isinstance(type_name, str) and len(type_name) > 0, "The cnvt_name should be given"
        
        func_wrap = lambda *args, **kwargs : cnvt_func(*args, **kwargs)
        self.__customized_cnvtor[type_name] = func_wrap