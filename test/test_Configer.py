from easy_config.Configer import Configer
from test_flag import get_flag_from_ext

if __name__ == '__main__':
    cfger = Configer()
    cfger.cfg_from_ini("./simple_test.ini")
    flg = cfger.get_cfg_flag()
    print(flg.ModelSpecification)
    print(get_flag_from_ext().ModelSpecification)
    