import unittest

from easy_config.Configer import Configer
from easy_config.IO_Converter import IO_Converter

import argparse 

class IO_ConverterTestCase(unittest.TestCase):

    def setUp(self):
        self.cfger = Configer()
        self.cfger.cfg_from_ini("./test_cfg_a.ini")
        self.cfger.cfg_from_str(self._build_cfg_text())

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
    
    def test_io_convter(self):
        cfg_cnvter = IO_Converter()
        
        argp_cfg = cfg_cnvter.cnvt_cfg(self.cfger, 'argparse')
        ome_cfg = cfg_cnvter.cnvt_cfg(self.cfger, 'omegacfg')
        yaml_cfg = cfg_cnvter.cnvt_cfg(self.cfger, 'yaml')
        
        self.assertEqual(type(argp_cfg), argparse.Namespace)
        self.assertEqual(ome_cfg.Section_test_B.fflg, False)
        self.assertEqual(type(yaml_cfg), str)

if __name__ == '__main__':
    tests = ['test_io_convter']
    suite = unittest.TestSuite(map(IO_ConverterTestCase, tests))
    unittest.main(verbosity=2)