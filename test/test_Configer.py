from easy_config.Configer import Configer
from test_flag import get_flag_from_ext

class test(object):    
    def __init__(self, num, name):
        self.num = num
        self.name = name

    def num_name(self):
        return self.num * self.name

if __name__ == '__main__':
    cfger = Configer()
    cfger.regist_cnvtor('tst_cls', test)
    cfger.cfg_from_ini("./simple_test.ini")
    print(cfger.dum.num_name())

    flg = cfger.get_cfg_flag()
    print(flg.ModelSpecification)
    print(get_flag_from_ext().ModelSpecification)