from easy_configer.Configer import Configer

def build_cfg_text_a():
    return '''
    # Initial config file :
    inpo = 46@int
    [test]         
        mrg_var_tst = [1, 3, 5]
        tst_var = {'kk':56, 'pp':'josef'}@tst_cls
        [test.ggap]
            gtgt = 'haha'

    [ghyu]
        [ghyu.opop]
            add = 32
            [ghyu.opop.tueo]
                salt = $inpo

    # Cell cfg written by Josef-Huang..
    '''

def build_cfg_text_b():
    return '''
    # Initial config file :
    inop = 32@int
    [test]         
        mrg_var_tst = [1, 3, 5]
        [test.ggap]
            gtgt = 'overrides'
            [test.ggap.conf]
                secert = 42

    [ghyu]
        [ghyu.opop]
            add = 67
            div = 1e-4

    [new]
        [new.new]
            newsec = 'wpeo'
    # Cell cfg written by Josef-Huang..
    '''

class Tst_cls:
    def __init__(self, kk, pp):
        self.kk = kk
        self.pp = pp
    
    def get_pp(self):
        return self.pp * 2

if __name__ == "__main__":
    cfg_a = Configer(cmd_args=True)
    cfg_a.regist_cnvtor("tst_cls", Tst_cls)  # regist customer class
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