import unittest

from easy_configer.Configer import Configer
from .get_flag import get_flag_from_ext

class test(object):    
    def __init__(self, num, string):
        self.num = num
        self.name = string

    def num_name(self):
        return self.num * self.name

class ConfigerTestCase(unittest.TestCase):
    
    def setUp(self):
        self.cfgerA = Configer()
        self.cfgerB = Configer()
        self.cfgerC = Configer()

    def _build_cfg_text(self):
        return '''
        # Initial config file :
        [Section_test_A]         
        mrg_var_tst = fromBcfg@str

        [Section_test_B]
        fflg = False@bool   # test inline comment in cfg-str
        tflg = True@bool
        # Cell cfg written by Josef-Huang..
        '''
    
    def test_parse_config(self):
        self.cfgerA.cfg_from_ini("./test_cfg_a.ini")
        raw_cfg_text = self._build_cfg_text()
        self.cfgerB.cfg_from_str(raw_cfg_text)

        # Basic test for config A
        self.assertEqual(type(self.cfgerA.Section_test_A), dict)
        self.assertEqual(self.cfgerA.Section_test_A['sec_var_tst'], "test")
        self.assertEqual(self.cfgerA.Section_test_A['tst_ext_var'], self.cfgerA.flt_var)
        
        # Basic test for config B
        self.assertEqual(type(self.cfgerB.Section_test_B), dict)
        self.assertEqual(self.cfgerB.Section_test_B['fflg'], False)
        self.assertEqual(self.cfgerB.Section_test_A['mrg_var_tst'], 'fromBcfg')

    def test_merge_config(self):
        self.cfgerA.cfg_from_ini("./test_cfg_a.ini")
        raw_cfg_text = self._build_cfg_text()
        self.cfgerB.cfg_from_str(raw_cfg_text)

        self.cfgerA.merge_conf(self.cfgerB, override=True)
        # after merging, secB should in cfgerA, the var should be replaced!!
        self.assertIn('Section_test_B', self.cfgerA.__dict__)
        self.assertEqual(self.cfgerA.Section_test_A['mrg_var_tst'], 'fromBcfg')

    def test_concate_config(self):
        self.cfgerA.cfg_from_ini("./test_cfg_a.ini")
        raw_cfg_text = self._build_cfg_text()
        self.cfgerB.cfg_from_str(raw_cfg_text)

        merge_conf = self.cfgerA.concate_cfg(self.cfgerB, override=True)
        self.assertIn('Section_test_B', merge_conf.__dict__)
        self.assertNotIn('Section_test_B', self.cfgerA.__dict__)
        self.assertNotEqual(self.cfgerA.Section_test_A['mrg_var_tst'], 'fromBcfg')

    def test_self_regist_cls(self):
        self.cfgerC.regist_cnvtor('tst_cls', test)
        self.cfgerC.cfg_from_ini("./test_cfg_reg.ini")
        # test dummy class
        self.assertEqual(type(self.cfgerC.dummy), test)
        self.assertEqual(self.cfgerC.dummy.name, 'josef')
        self.assertEqual(self.cfgerC.Section_test_A['dummy'].num_name(), 3*'ulala')

if __name__ == '__main__':
    tests = ['test_parse_config', 'test_merge_config', 'test_self_regist_cls']
    suite = unittest.TestSuite(map(ConfigerTestCase, tests))
    unittest.main(verbosity=2)