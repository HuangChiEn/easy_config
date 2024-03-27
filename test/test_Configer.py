import unittest

from easy_configer.Configer import Configer
from easy_configer.utils.Container import AttributeDict

from .test_properties.test_object import Customized_Object, get_cfg_str, get_flag


class ConfigerTestCase(unittest.TestCase):
    
    def setUp(self):
        # init configer
        self.cfg1 = Configer()
        self.cfg2 = Configer()
        self.cfg3 = Configer()

        # declare config we're going to test
        self.dtype_cfg_path = 'test/test_properties/dtype_cfg.ini'   
        self.hier_cfg_path = 'test/test_properties/hier_cfg.ini'
        self.sub_cfg_path = 'test/test_properties/sub_cfg.ini'

        self.init_cfg_path = 'test/test_properties/init_cfg.ini'
        self.merg_cfg_path = 'test/test_properties/merg_cfg.ini'

    def test_parsing_config(self):
        # test dtype decleration
        self.cfg2.cfg_from_ini(self.dtype_cfg_path)
        cfg_str = get_cfg_str(self.dtype_cfg_path)
        self.cfg1.cfg_from_str(cfg_str)
        
        self._test_dtype(self.cfg1)
        self._test_dtype(self.cfg2)
        # test hier 
        self.cfg1.cfg_from_ini(self.hier_cfg_path)
        self._test_hier(self.cfg1)
        # test sub-config
        self.cfg2.cfg_from_ini(self.sub_cfg_path)
        self._test_subcfg(self.cfg2)

    def _test_dtype(self, cfg):
        self.assertEqual(cfg.i_var1, 42)
        self.assertEqual(cfg.i_var_neg, -42)
        self.assertEqual(cfg.i_var1, cfg.i_var2)

        self.assertLess( (cfg.f_var1-cfg.f_var2),  1e-7)

        self.assertEqual(cfg.s_var1, 'test')
        self.assertEqual(cfg.s_var1, cfg.s_var2)

        self.assertEqual(cfg.b_var1, True)
        self.assertEqual(cfg.b_var1, (not cfg.b_var2))

        self.assertEqual(cfg.n_var, None)

        self.assertEqual(cfg.l_var1, [1, 3, 5])
        self.assertEqual(cfg.l_var1, cfg.l_var2)

        self.assertEqual(cfg.t_var1, (1, 3, 5))
        self.assertEqual(cfg.t_var1, cfg.t_var2)

        self.assertEqual(cfg.st_var1, {1, 3, 5})
        self.assertEqual(cfg.st_var1, cfg.st_var2)

        self.assertEqual(cfg.d_var1, {'tst':42, 'kkk':-1})
        self.assertEqual(cfg.d_var1, cfg.d_var2)

    def _test_hier(self, cfg):
        self.assertIsInstance(cfg.sec1, AttributeDict)
        self.assertIn('sec21', cfg.sec1)
        self.assertIn('sec22', cfg.sec1)
        
        self.assertIsInstance(cfg.sec1.sec21, AttributeDict)
        self.assertIn('sec21_var', cfg.sec1.sec21)

        self.assertIn('secB', cfg.secA)
        self.assertIn('secC', cfg.secA.secB)
        self.assertIn('secD', cfg.secA.secB.secC)
        self.assertIsInstance(cfg.secA.secB.secC.secD, AttributeDict)
        self.assertEqual(cfg.secA.secB.secC.secD.lev, 4)

    def _test_subcfg(self, cfg):
        ## Note : cfg is not AttributeDict, so we use __dict__ to test it 
        # section in sub-config do exists
        self.assertIn('sec1', iter(cfg))
        # new defined section exists
        self.assertIn('sec_new', iter(cfg))
        # sub-config var 
        self.assertEqual(cfg.secA.secB.secC.lev, 3)
        
    def test_regist_cls(self):
        self.cfg1.regist_cnvtor('tst_cls', Customized_Object)
        self.cfg1.cfg_from_str("cust_var = {'arg1':True, 'tst':42}@tst_cls")
        
        self.assertIsInstance(self.cfg1.cust_var, Customized_Object)
        args = self.cfg1.cust_var.get_args()
        self.assertEqual(args[0], True)
        self.assertEqual(args[1], None)
        self.assertEqual(self.cfg1.cust_var.get_kw_args()['tst'], 42)

        self.cfg1.cfg_from_str("cust_var = [-1, -1, 42, 38, 96]@tst_cls")
        self.assertEqual(self.cfg1.cust_var.get_args(), (-1, -1))
        self.assertEqual(self.cfg1.cust_var.get_lst_args(), (42, 38, 96))

    def test_merge_config(self):
        self.cfg1.cfg_from_ini(self.init_cfg_path)
        self.cfg2.cfg_from_ini(self.merg_cfg_path)
        
        # | or operator, the return cfg is deepcopy.. not affect original cfg
        # cfg1 should be overrided
        overrided_cfg1 = self.cfg1 | self.cfg2
        self._test_or_config(overrided_cfg1)

        # + add operator, cfg1 should NOT be overrided!!
        with self.assertRaisesRegex(RuntimeError, 'input config already exists in merged config') as cm:
            overrided_cfg1 = self.cfg1 + self.cfg2
        
        # remove the conflict keys & sections
        del self.cfg2.sec1 ; del self.cfg2.override_var
        overrided_cfg1 = self.cfg1 | self.cfg2
        self._test_concate_config(overrided_cfg1)

    def _test_or_config(self, cfg):
        # after merging, new section appears
        self.assertIn('new_sec2', cfg)
        self.assertEqual(cfg.new_sec2.var, 42)
        # after merging, some var has been overrided
        self.assertEqual(cfg.override_var, 42)
        self.assertEqual(cfg.sec1.sec2.override_var, 42)
        # after merging, non-redefined var should keep the same
        self.assertEqual(cfg.init_var, 'init')
        self.assertEqual(cfg.new_sec1.var, -1)

    def _test_concate_config(self, cfg):
        # after merging, new section appears
        self.assertIn('new_sec2', cfg)
        self.assertEqual(cfg.new_sec2.var, 42)
        self.assertEqual(cfg.override_var, -1)
        self.assertEqual(cfg.merg_var, 'merge')
    
    def test_cmd_args(self):
        self._simulate_cmd_args()
        # since `cmd_args=False` in default, config from client args will be ignored!
        # it should raise the warning..
        with self.assertWarns(Warning):
            self.cfg2.cfg_from_cli()
        
        self.assertNotIn('init_var', self.cfg2)
        # override flatten variable
        self.assertEqual(self.cfg2.override_var, 42)
        # override hierachical variable
        self.assertEqual(self.cfg2.sec1.sec2.override_var, 42)
        # add new flatten variable
        self.assertEqual(self.cfg2.new_var, 42)
        # add new variable in section
        self.assertEqual(self.cfg2.new_sec.new_var, 42)

        self.cfg4 = Configer(description='Test config', cmd_args=True)
        self.cfg4.cfg_from_ini(self.init_cfg_path)

        # override flatten variable
        self.assertEqual(self.cfg4.override_var, 42)
        # override hierachical variable
        self.assertEqual(self.cfg4.sec1.sec2.override_var, 42)
        # add new flatten variable
        self.assertEqual(self.cfg4.new_var, 42)
        # add new variable in section
        self.assertEqual(self.cfg4.new_sec.new_var, 42)

        self.cfg5 = Configer(description='Test config', cmd_args=False)
        self.cfg5.cfg_from_ini(self.init_cfg_path)
        # since `cmd_args=False`, all args should keep identitcal as initial config!
        self.assertEqual(self.cfg5.override_var, -1)
        self.assertEqual(self.cfg5.sec1.sec2.override_var, -1)
        self.assertNotIn('new_var', self.cfg5)
        self.assertNotIn('new_var', self.cfg5.new_sec1)

    def _simulate_cmd_args(self):
        import sys
        # test override the default args
        sys.argv.pop(0)  # remove `python -m unittest` cmd, it'll not given 
        sys.argv.extend([
            'override_var=42',   
            'sec1.sec2.override_var=42',  
            'new_var=42',  
            'new_sec.new_var=42',
            '-h'  # print description
        ])

    def test_flag(self):
        self.cfg1.cfg_from_ini(self.init_cfg_path)
        absl_flag = get_flag()

        # absl_flag will get the identical cfg of configer
        self.assertEqual(self.cfg1.override_var, absl_flag.override_var)
        self.assertEqual(self.cfg1.sec1.sec2.override_var, absl_flag.sec1.sec2.override_var)
        self.assertEqual(self.cfg1.init_var, absl_flag.init_var)
        self.assertEqual(self.cfg1.new_sec1.var, absl_flag.new_sec1.var)


if __name__ == '__main__':
    tests = ['test_parsing_config', 'test_regist_cls', 'test_merge_config', 'test_cmd_args']
    suite = unittest.TestSuite(map(ConfigerTestCase, tests))
    unittest.main(verbosity=2)