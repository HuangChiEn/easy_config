from copy import deepcopy

class AttributeDict(dict):
    '''
    A dict-like container to store nested arguments defined in config.
    Since the container inherit python native dict (base class), we simply store 
    arguments in the base dict with such navie way : `dict[key] = value`,
    by calling super().__setitem__(key, value) in subclass. self.__setattr__ 
    also call super().__setitem__ underhood! According to the way we store args, 
    we access args by the navie way self[key] (namely, dict[key]). 
    Additionally, we build the getattr guard for implement the defaultdict functionality.
    self.__getitem__ no need to override, just as same as base class.
    '''

    def __init__(self, init_dict={}):
        ''' 
        Constructor of container. 
        
        Args: 
            init_dict (dict): typically it'll be value dict parsed in Configer. Default to empty dict.
        
        Return:
            None.
        '''
        self.set_attr_dict(init_dict)
    
    def __getattribute__(self, attr):
        '''
        Override __getattribute__ dunder method. Since we apply base class (dict) 
        to store all args, self.__dict__ should not be used in anyway.

        Raise:
            Runtime Error, while user attempt to access self.__dict__.
        '''
        if '__dict__' == attr:
            raise RuntimeError("Built in __dict__ can not be visited in AttributeDict")
        return super().__getattribute__(attr) #object.__getattribute__(self, attr)

    def __getattr__(self, key):
        '''
        Override __getattr__ dunder method to silently build the 'empty dict'. 
        So that we can assign value to the specific argument without define their parent dict.
        Note : same behavior as defaultdict, allow recursively self.__setattr__.

        Return:
            AttributeDict, the returned dict have pre-defined empty dict, 
            then the specific argument could be updated to the empty dict.
        '''
        
        try:
            return self[key]
        except:
            # the behavior different from defaultdict, raise attribute error..
            raise AttributeError("AttributeDict doesn't have the attribute {}".format(key))

    def set_attr_dict(self, raw_dict):
        ''' 
        Make input dict become AttributeDict instance, call __setitem__ underhood. 
        
        Args:
            raw_dict (dict): python native dict, it'll be turn into AttributeDict after calling this method.
        '''
        for k, v in raw_dict.items():
            self.__setitem__(k, v)
    
    def __setattr__(self, key, value):
        ''' Override __setattr__ dunder method. call __setitem__ underhood. '''
        self[key] = value
    
    def __setitem__(self, key, value):
        ''' Override __setitem__ dunder method. Wrap any input value with AttributeDict container. '''
        if isinstance(value, dict):
            value = AttributeDict(value)
        # ? base class is dict, actually we store all args in dict object
        super().__setitem__(key, value)

    def __deepcopy__(self, memo=None):
        ''' Support deepcopy, src:https://stackoverflow.com/questions/49901590/python-using-copy-deepcopy-on-dotdict. '''
        return AttributeDict(deepcopy(dict(self), memo=memo))

    def __getstate__(self):
        ''' Basic serialized interface (i.e. pickle). Return serielized python object. '''
        return self
    
    def __setstate__(self, de_ser_self):
        ''' Basic serialized interface (i.e. pickle). Accept de-serielized object, replace default self into it. '''
        self = de_ser_self


class Flag(object):
    '''
    A synchronized object to defined config in Configer. It's inspired by absl flag in tensorflow. 
    Although this is not useful, but we keep this class for competible with easy_config early version.
    You still can use it.
    '''
    _singleton_inst = None
    def __new__(cls, *args, **kwargs): 
        ''' 
        Override __new__ dunder method. __new__ is used to create the class before calling __init__,
        so we set the singleton guard in here for implement the singleton design pattern.
        
        Args:
            *args, **kwargs : will be passed into FLAG_spec instance, which is the singleton instance.
        
        Return:
            FLAG_spec, a sync object of config.
        '''
        # new a instance, if no instance have been created 
        if cls._singleton_inst is None:     
            # store 'the' instance into staitc member
            cls._singleton_inst = super().__new__(cls) 
            # create the 'common' flag space allow all instance access
            cls.flag_spec = type("FLAG_spec", (), {})()
        # next time create the other instance, 
        # just let it point to 'the' singleton instance!
        return cls._singleton_inst
  
    @property
    def FLAGS(self):
        ''' Interface to access FLAG_spec object. '''
        return self.flag_spec

if __name__ == "__main__":
    tmp = AttributeDict({'kk':45, 'bb':{'jj':{'gg':42}, 'kk':32}})
    breakpoint()