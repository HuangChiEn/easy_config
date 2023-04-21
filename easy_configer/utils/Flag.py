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