from easy_configer.Configer import Configer

def build_cfg_text_a():
    return '''
    # Initial config file :
    inpo = 46@int
    [test]         
        mrg_var_tst = [1, 3, 5]@list
        [test.ggap]
            gtgt = haha@str

    [ghyu]
        [ghyu.opop]
            add = 32@int
            [ghyu.opop.tueo]
                salt = $inpo

    # Cell cfg written by Josef-Huang..
    '''

def build_cfg_text_b():
    return '''
    # Initial config file :
    inop = 32@int
    [test]         
        mrg_var_tst = [1, 3, 5]@list
        [test.ggap]
            gtgt = overrides@str
            [test.ggap.conf]
                secert = 42@int

    [ghyu]
        [ghyu.opop]
            add = 67@int
            div = 1e-4@float

    [new]
        [new.new]
            newsec = wpeo@str
    # Cell cfg written by Josef-Huang..
    '''

if __name__ == "__main__":
    cfg_a = Configer(cmd_args=True)
    cfg_a.cfg_from_str(build_cfg_text_a())  
    

    cfg_b = Configer()
    cfg_b.cfg_from_str(build_cfg_text_b())

    #cfg_a.merge_conf(cfg_b, override=True)
    cfg_b |= cfg_a
    
    # Note that you can use :
    #   python test.py test.mrg_var_tst "{'yeah':'success'}@dict" 
    #   to change the any default value in commend-line!!
    print(cfg_a)
    breakpoint()