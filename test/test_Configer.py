from easy_config.Configer import Configer
from test import tt
if __name__ == '__main__':
    cfger = Configer()
    cfger.cfg_from_ini("./simple_test.ini")
    flg = cfger.get_cfg_flag()
    print(flg.ModelSpecification)
    print(tt().ModelSpecification)
    