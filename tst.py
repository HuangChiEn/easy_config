def build_cfg_text_a():
    return '''
    # defined as pure python dict object
    tst_dct = { \
        'kk' : 'aoa', \
        'bp' : True \
    }
    kk = {'tmp':52, 'gg':128}  # @dict will also fine ~

    # Initial config file :
    tst = False @bool
    inpo = 46@int
    > ./test/test_properties/hier_cfg.ini

    # hierachical section will be considered as 
    # the special nested dict (AttributeDict)
    [test]         
        mrg_tst_var = [1, 3, 5]
        [test.ggap]
            gtgt = $sec1.sec21.sec21_var
    [ghyu]
        [ghyu.opop]
            add = 32
            [ghyu.opop.tueo]
                salt = $test.ggap.gtgt
        
    # Cell cfg written by Josef-Huang..
    '''


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
    

if __name__ == "__main__":
    #tst = {'tt':5, 'kk':{'gg':6}}
    #dct = AttributeDict(tst)

    #dct = dotmap(tst)
    #breakpoint()
    
    from easy_configer.Configer import Configer
    from test.test_properties.test_object import Customized_Object

    cfg = Configer(cmd_args=True)
        
    cfg.cfg_from_str(build_cfg_text_a())
    cfg.regist_cnvtor('tst_cls', Customized_Object)

    #cfg.cfg_from_ini('./test/test_properties/dtype_cfg.ini')
    
    breakpoint()

    