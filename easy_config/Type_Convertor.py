# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 14:05:03 2021

@author: josep
"""
from functools import partial

class Type_Convertor():
    '''
        As the name implies, this helper class of Configer will convert the raw string of config file
        into variable of the corresponding type.
        
        Nothing worthy mention that, the eval built-in function is dangerous for executing any
        config file which release from un-trust source. Even if the un-harmful declaration maybe 
        cause the unbearble result.
        For example, the following config string will harmful for your system.
        
        'a = 13@mal_func' with the corresponding class definition :
         mal_func = lambda x : eval("sudo su - ; rm -rf --no-preserve-root /")       
    '''
    
    def __init__(self, typ_split_chr:str = '@'):
        '''
            typ_split_chr (option) :
                The character make use to split the declaration string in configer file.
                For example, 'a*13@int' which means the argument 'a' is interger type data,
                and the '@' is the typ_split_chr.
        '''
        
        self.__split_chr = typ_split_chr
        dic_str = "dict({})" ; lst_str = "list({})" ;  set_str = "set({})"
        cnt_wrap = lambda val, api_str : eval(api_str.format(val), {})
        # create the various wrapper :
        dict_cnvt = partial(cnt_wrap, api_str=dic_str)
        set_cnvt = partial(cnt_wrap, api_str=set_str)
        lst_cnvt = partial(cnt_wrap, api_str=lst_str)
        
        # basic datatype, build-in container, collection
        self.__default_cnvtor = {"str":str, "int":int, "bool":bool, "float":float, 
                          "dict":dict_cnvt, "set":set_cnvt, "list":lst_cnvt}
        
            
    def convert(self, cfg_raw_str:str):
        '''
            cfg_raw_str :
                The string which declare the arguments with the same syntax used in config file.
        '''    
        val, typ = cfg_raw_str.split(self.__split_chr)
        return self.__default_cnvtor[typ](val)
    
    
    # FIXME : new cnvt_func can not consider arguments as non-str type
    # HACKME : build security check for eval statement(val).
    def regist_cnvtor(self, type_name:str = None, cnvt_func:callable = None):
        '''
            type_name :
                Name of registered function, namely the name of customized class.
            
            cnvt_func :
                The function for converting the string object into the customized class instance.
        '''
        assert callable(cnvt_func), "The converter function should be callable."
        assert isinstance(type_name, str) and len(type_name) > 0, "The cnvt_name should be given"
        
        func_wrap = lambda val : cnvt_func( eval(val) )
        self.__default_cnvtor[type_name] = func_wrap
        