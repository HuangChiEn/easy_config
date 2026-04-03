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
        self.cfg4 = Configer()
        
        # declare config we're going to test
        self.dtype_cfg_path = 'test/test_properties/dtype_cfg.ini'   
        self.hier_cfg_path = 'test/test_properties/hier_cfg.ini'
        self.sub_cfg_path = 'test/test_properties/sub_cfg.ini'
        self.nested_sub_cfg_path = 'test/test_properties/nested_sub_cfg.ini'

        self.init_cfg_path = 'test/test_properties/init_cfg.ini'
        self.merg_cfg_path = 'test/test_properties/merg_cfg.ini'

        self.resolve_cfg_path = 'test/test_properties/reslv_cfg.ini'
        self.post_filter_cfg_path = 'test/test_properties/filter_cfg.ini'

    def test_parsing_config(self):
        # test equivalent of string / file reading
        #   get_cfg_str apply open, f_ptr.read into str
        cfg_str = get_cfg_str(self.dtype_cfg_path)
        self.cfg1.cfg_from_str(cfg_str)
        self.cfg2.cfg_from_ini(self.dtype_cfg_path)
        # test dtype decleration
        self._test_dtype(self.cfg1)
        self._test_dtype(self.cfg2)
        
        # test hier 
        self.cfg1.cfg_from_ini(self.hier_cfg_path)
        self._test_hier(self.cfg1)

        # Given the same config!
        # the argument can not be overwrited in the identitcal config!
        with self.assertRaisesRegex(RuntimeError, 'Re-define Error') as cm:
            self.cfg1.cfg_from_str("i_var1 = -1")

        # define new var in already defined section should be allowed!
        sl_cfg_str = 'new_var = 42'
        self.cfg1.cfg_from_str(f'''
            [secA]
                {sl_cfg_str}
        ''')
        self.assertEqual(self.cfg1.secA.new_var, int(sl_cfg_str.split('=')[-1]))
        
        with self.assertRaisesRegex(RuntimeError, 'Re-define Error') as cm:
        # test hierachical var be redefined!
            self.cfg1.cfg_from_str('''
                [secA]
                    lev = 42
            ''')

        # test allow_overwrite flag for cfg_from_str & cfg_from_ini 
        sl_cfg_str = 'i_var1 = -1'
        self.cfg1.cfg_from_str(sl_cfg_str, allow_overwrite=True)
        self.assertEqual(self.cfg1.i_var1, int(sl_cfg_str.split('=')[-1]))

        self.cfg1.cfg_from_ini(self.dtype_cfg_path, allow_overwrite=True)
        self.assertEqual(self.cfg1.i_var1, 42)

        # test erro raised by non-overwrite sub-config
        with self.assertRaisesRegex(RuntimeError, 'Re-define Error') as cm:
            self.cfg3.cfg_from_ini(self.sub_cfg_path)
        
        # test overwrite sub-config (same as dynamic config loading in omegaconf!)
        # Note : `allow_overwrite=True` let overwrite from client arguments & subconfig
        self.cfg4.cfg_from_ini(self.sub_cfg_path, allow_overwrite=True)
        self._test_subcfg(self.cfg4)

    def _test_dtype(self, cfg):
        # chk type
        self.assertIsInstance(cfg.i_var1, int)
        # chk value
        self.assertEqual(cfg.i_var1, 42)
        # chk negative
        self.assertEqual(cfg.i_var_neg, -42)
        # chk equivalent
        self.assertEqual(cfg.i_var1, cfg.i_var2)

        self.assertIsInstance(cfg.f_var1, float)
        self.assertLess( (cfg.f_var1-cfg.f_var2),  1e-7)

        self.assertIsInstance(cfg.s_var1, str)
        self.assertEqual(cfg.s_var1, 'test')
        self.assertEqual(cfg.s_var1, cfg.s_var2)

        self.assertIsInstance(cfg.b_var1, bool)
        self.assertEqual(cfg.b_var1, True)
        self.assertEqual(cfg.b_var1, (not cfg.b_var2))

        self.assertIsInstance(cfg.n_var, type(None))
        self.assertEqual(cfg.n_var, None)

        self.assertIsInstance(cfg.l_var1, list)
        self.assertEqual(cfg.l_var1, [1, 3, 5])
        self.assertEqual(cfg.l_var1, cfg.l_var2)

        self.assertIsInstance(cfg.t_var1, tuple)
        self.assertEqual(cfg.t_var1, (1, 3, 5))
        self.assertEqual(cfg.t_var1, cfg.t_var2)

        self.assertIsInstance(cfg.st_var1, set)
        self.assertEqual(cfg.st_var1, {1, 3, 5})
        self.assertEqual(cfg.st_var1, cfg.st_var2)

        self.assertIsInstance(cfg.d_var1, dict)
        self.assertEqual(cfg.d_var1, {'tst':42, 'kkk':-1})
        self.assertEqual(cfg.d_var1, cfg.d_var2)

        # muti-line declaration
        self.assertIsInstance(cfg.ml_var1, list)
        self.assertEqual(cfg.ml_var1, cfg.ml_var2)
        self.assertEqual(cfg.ml_var1, cfg.ml_var3)
        self.assertEqual(cfg.ml_var1, cfg.ml_var4)

        self.assertIsInstance(cfg.mt_var1, tuple)
        self.assertIsInstance(cfg.ms_var1, set)
        self.assertIsInstance(cfg.md_var1, dict)

        # nested objects declaration in multiple line
        self.assertEqual(cfg.nsl_var1, [[[1, 3, 5]]])
        self.assertEqual(cfg.nsl_var2, [[1, 3, [5]]])
        self.assertEqual(cfg.nsl_var3, [(1, 3, 5), {2, 4, 6}])
        self.assertEqual(cfg.nsl_var4, [1, (3, 5), {2, 4}, 6])
        self.assertEqual(cfg.nsd_var1, {'d_1':{'v_1':True, 'v_2':[1, 3, 5], 'v_3':(2, 4, 6)}})

    def _test_hier(self, cfg):
        ## Note : cfg is not AttributeDict, due to hist reason
        self.assertIsInstance(cfg, Configer)
        self.assertIn('sec1', iter(cfg))
        self.assertIn('secA', iter(cfg))

        # test hier-containers are AttributeDict!
        self.assertIsInstance(cfg.sec1, AttributeDict)
        self.assertIn('sec21', cfg.sec1)
        self.assertIn('sec22', cfg.sec1)
        self.assertIsInstance(cfg.sec1.sec21, AttributeDict)
        self.assertIn('sec21_var', cfg.sec1.sec21)
        # dot access
        self.assertEqual(cfg.sec1.sec21.sec21_var, 42)
        # dict key access
        self.assertEqual(cfg['sec1']['sec21']['sec21_var'], 42)
        # interleave access
        self.assertEqual(cfg.sec1['sec21'].sec21_var, 42)
        # depth test
        self.assertIn('secB', cfg.secA)
        self.assertIn('secC', cfg.secA.secB)
        self.assertIn('secD', cfg.secA.secB.secC)
        self.assertIsInstance(cfg.secA.secB.secC.secD, AttributeDict)
        self.assertEqual(cfg.secA.secB.secC.secD.lev, 4)

    def _test_subcfg(self, cfg):
        # assert default value had been overwrite
        self.assertEqual('from_dummy', cfg.ori_var)

        ## Note : cfg is not AttributeDict, so we use __dict__ to test it 
        # section in recur_sub_cfg 
        self.assertIn('recur_sec', iter(cfg))
        
        # The recommended way to load a sub-config :
        #   define a new section for storing the sub-config to prevent section conflict!!
        # If you want to overwrite the original config by using subconfig mechanism, 
        #   enable `allow_overwrite=True`
        self.assertIn('hier_sec', iter(cfg))

        # sub-config var 
        self.assertEqual(cfg.hier_sec.secA.secB.secC.lev, 3)

        # testing nested sub-config overwrite
        self.assertEqual(cfg.overwrite_sec.ori_var, 'from_dummy')
        
    def test_regist_cls(self):
        self.cfg1.regist_cnvtor('tst_cls', Customized_Object)
        self.cfg1.cfg_from_str("cust_var = {'arg1':True, 'tst':42}@tst_cls")
        
        self.assertIsInstance(self.cfg1.cust_var, Customized_Object)
        args = self.cfg1.cust_var.get_args()
        self.assertEqual(args[0], True)
        self.assertEqual(args[1], None)
        self.assertEqual(self.cfg1.cust_var.get_kw_args()['tst'], 42)

        self.cfg2.regist_cnvtor('tst_cls', Customized_Object)
        self.cfg2.cfg_from_str("cust_var = [-1, -1, 42, 38, 96]@tst_cls")
        self.assertEqual(self.cfg2.cust_var.get_args(), (-1, -1))
        self.assertEqual(self.cfg2.cust_var.get_lst_args(), (42, 38, 96))

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
        lst_cmd = [
            'override_var=42',   
            'sec1.sec2.override_var=42',  
            'new_var=42',  
            'new_sec1.new_var=42',
            '-h'  # print description
        ]
        self._simulate_cmd_args(lst_cmd)

        # Test empty cfg, args only from client input
        self.cfg1.cfg_from_cli()
        # add new flatten variable
        self.assertEqual(self.cfg1.new_var, 42)
        # add new variable in hier section
        self.assertEqual(self.cfg1.new_sec1.new_var, 42)
        
        # Test client input args override cfg from init
        self.ini_cfg = Configer(description='Test config', cmd_args=True)
        self.ini_cfg.cfg_from_ini(self.init_cfg_path)
        
        # override flatten variable
        self.assertEqual(self.ini_cfg.override_var, 42)
        # override hierachical variable
        self.assertEqual(self.ini_cfg.sec1.sec2.override_var, 42)
        # preserve original var
        self.assertEqual(self.ini_cfg.new_sec1.var, -1)

        self.only_ini_cfg = Configer(cmd_args=False)
        self.only_ini_cfg.cfg_from_ini(self.init_cfg_path)
        # since `cmd_args=False`, all args should keep identitcal as initial config!
        self.assertEqual(self.only_ini_cfg.override_var, -1)
        self.assertEqual(self.only_ini_cfg.sec1.sec2.override_var, -1)
        self.assertNotIn('new_var', self.only_ini_cfg)
        self.assertNotIn('new_var', self.only_ini_cfg.new_sec1)

        # Test client input args intend to change section itself
        self._simulate_cmd_args(['sec1.sec2=None'], clear_all=True)
        self.sec_cfg = Configer(cmd_args=True)
        with self.assertRaisesRegex(RuntimeError, 'overwrite pre-defined section') as cm:
            self.sec_cfg.cfg_from_ini(self.init_cfg_path, allow_overwrite=False)

        with self.assertRaisesRegex(RuntimeError, 'overwrite pre-defined section') as cm:        
            # Note. we change unexpected behavior, now client args should not overwrite sec!
            self.sec_cfg.cfg_from_ini(self.init_cfg_path, allow_overwrite=True)
        
        self.assertNotEqual(self.sec_cfg.sec1.sec2, None)

    def _simulate_cmd_args(self, lst_cmd, clear_all=False):
        import sys
        # remove all previous defined arguments..
        sys.argv = [] if clear_all else sys.argv
        sys.argv.extend(lst_cmd)

    def test_flag(self):
        self.cfg1.cfg_from_ini(self.init_cfg_path)
        absl_flag = get_flag()

        # absl_flag will get the identical cfg of configer
        self.assertEqual(self.cfg1.override_var, absl_flag.override_var)
        self.assertEqual(self.cfg1.sec1.sec2.override_var, absl_flag.sec1.sec2.override_var)
        self.assertEqual(self.cfg1.init_var, absl_flag.init_var)
        self.assertEqual(self.cfg1.new_sec1.var, absl_flag.new_sec1.var)    

    def test_config_resolve(self):
        self.cfg1.cfg_from_ini(self.resolve_cfg_path)
        self.assertEqual(self.cfg1.flat_var, self.cfg1.dup_var)

        self.assertEqual(self.cfg1.sec1.sec2.intp_var, '/root/workspace/tmp')
        self.assertEqual(self.cfg1.new_sec1.var, '/root/workspace/tmp/kkk')
        
        # resolve argument, it should same as the argument
        self.assertEqual(self.cfg1.new_sec1.new_var, self.cfg1.new_sec1.var)
        self.assertEqual(self.cfg1.new_sec1.new_num, self.cfg1.sec1.sec2.num)

    def test_filter(self):
        self.cfg1.regist_lambda('addtwo', lambda x : x + 2)
        self.cfg1.cfg_from_ini(self.post_filter_cfg_path)
        
        # test string-type builtin post-processor
        self.assertTrue(self.cfg1.upper_var.isupper())
        self.assertTrue(self.cfg1.lower_var.islower())
        self.assertEqual(sum([ c.isspace() for c in self.cfg1.strip_var ]), 0)

        # test various type conversion
        self.assertIsInstance(self.cfg1.str_var, str)
        self.assertIsInstance(self.cfg1.bool_var, bool)
        self.assertIsInstance(self.cfg1.int_var, int)
        self.assertIsInstance(self.cfg1.float_var, float)

        # test regist filter
        self.assertEqual(self.cfg1.addtwo_var, self.cfg1.inp_var+2)
    

class ConfigerIntegrateTestCase(unittest.TestCase):
    
    def setUp(self):
        # init configer
        self.cfg = Configer(cmd_args=True)
        
        # declare config we're going to test
        self.resolve_cfg_path = 'test/test_properties/reslv_cfg.ini'
        self.post_filter_cfg_path = 'test/test_properties/filter_cfg.ini'

    def _simulate_cmd_args(self, lst_cmd, clear_all=False):
        import sys
        # remove all previous defined arguments..
        sys.argv = [] if clear_all else sys.argv
        sys.argv.extend(lst_cmd)

    def test_cli_update_interpolation(self):
        lst_cmd = [
            'flat_var=HiHi@str',   
            'sec1.sec2.num=-1',  
        ]
        self._simulate_cmd_args(lst_cmd)
        self.cfg.cfg_from_ini(self.resolve_cfg_path)
        
        # test real-time commendline update for interpolation
        self.assertEqual(self.cfg.dup_var, 'HiHi')
        self.assertEqual(self.cfg.sec1.sec2.intp_var, "/root/HiHi/tmp")

        self.assertEqual(self.cfg.sec1.sec2.num, -1)
        self.assertEqual(self.cfg.sec1.sec2.num, self.cfg.new_sec1.new_num)


if __name__ == '__main__':
    # test_cli_update_interpolation
    tests = ['test_parsing_config', 'test_regist_cls', 'test_merge_config', 'test_cmd_args', 'test_flag', 'test_config_resolve', 'test_filter']
    suite = unittest.TestSuite(map(ConfigerTestCase, tests))
    unittest.main(verbosity=2)