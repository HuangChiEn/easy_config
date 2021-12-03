from easy_config.Configer import Configer

if __name__ == '__main__':
    cfger = Configer()
    cfger.cfg_from_ini("./test/simple_test.ini")
    print(cfger)