# Similar with EasyDict, but we implement attr-dict in the other way
class AttributeDict(dict):

    def __init__(self, init_dict={}):
        self.set_attr_dict(init_dict)

    def __getattr__(self, key):
        try:
            return self[key]
        except:
            # same behavior as defaultdict, allow recursively self.__setattr__
            self[key] = AttributeDict({})
        return self[key]

    # make input dict become AttributeDict instance
    def set_attr_dict(self, raw_dict):
        for k, v in raw_dict.items():
            if isinstance(v, dict):
                self.__setitem__(k, AttributeDict(v))
            else:
                self.__setitem__(k, v)
    
    # also call self.__setitem__ underhood
    def __setattr__(self, key, value):
        self[key] = value
    
    # setitem via dict method will not turn input into AttributeDict
    def __setitem__(self, key, value):
        if isinstance(value, dict):
            value = AttributeDict(value)
        dict.__setitem__(self, key, value)


class Flag(object):
    _singleton_inst = None
    # __new__ is used to create the class before calling __init__,
    # so we set the singleton guard in here for implement the singleton design pattern
    def __new__(cls, *args, **kwargs): 
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
        return self.flag_spec