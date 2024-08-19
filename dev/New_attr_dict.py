class AttributeDict(dict):
    def __setitem__(self,name,value):
        print('__setitem__,')
        return super().__setitem__(name,value)

    def __getitem__(self,name):
        print('__getitem__, find in dict data-structure')
        return super().__getitem__(name)

    def __setattr__(self,name,value):
        print('__setattr__ , put name:value in instance.__dict__')
        return super().__setattr__(name,value)

    def __getattr__(self,name):
        print('__getattr__ if finally not find anything, come for me')
        try:
            # goto self.__getitem__
            value = self[name]
        except KeyError:
            print('None exsited key')
            return None
        if isinstance(value,dict):
            value = AttributeDict(value)
        return value
    def __getattribute__(self,name):
        print('__getarrtribute__ I handle all attribute at  very first')
        #通过object显示调用__getattr__
        # 如果不显示使用，除非属性找不到，否则不再调用__getattr__
        return object.__getattribute__(self,name)