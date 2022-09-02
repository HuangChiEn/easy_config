import unittest

from easy_config.Configer import Configer
from test_flag import get_flag_from_ext

class test(object):    
    def __init__(self, num, string):
        self.num = num
        self.name = string

    def num_name(self):
        return self.num * self.name

class ConfigerTestCase(unittest.TestCase):
    
    def setUp(self):
        self.cfger1 = Configer()
        self.cfger2 = Configer()
    
    def test_config(self):
        self.cfger1.cfg_from_ini("./test_cfg.ini")
        self.assertEqual(type(self.cfger1.Section_test1), dict)
        self.assertEqual(self.cfger1.Section_test1['sec_var_tst'], "test")
        self.assertEqual(self.cfger1.Section_test2['fflg'], False)

    def test_self_regist_cls(self):
        self.cfger2.regist_cnvtor('tst_cls', test)
        self.cfger2.cfg_from_ini("./test_reg_cfg.ini")
        self.assertEqual(type(self.cfger2.dummy), test)
        self.assertEqual(self.cfger2.dummy.num, 3)
        self.assertEqual(self.cfger2.dummy.num_name(), 3*'ulala')

if __name__ == '__main__':
    tests = ['test_config', 'test_self_regist_cls']
    suite = unittest.TestSuite(map(ConfigerTestCase, tests))
    unittest.main(verbosity=2)

    #flg = cfger.get_cfg_flag()
    #print(flg.ModelSpecification)
    #print(get_flag_from_ext().ModelSpecification)