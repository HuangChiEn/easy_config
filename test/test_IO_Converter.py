import unittest

from easy_configer.Configer import Configer
from easy_configer.IO_Converter import IO_Converter
from easy_configer.utils.Container import AttributeDict

import argparse 
import sys

from omegaconf.dictconfig import DictConfig
import yaml

from .test_properties.test_object import ServerConfig

class IO_ConverterTestCase(unittest.TestCase):

    def setUp(self):
        self.cfg1 = Configer()
        self.cfg_cnvter = IO_Converter()
        self.init_cfg_path = 'test/test_properties/init_cfg.ini'
       
    def test_convert_to(self):
        self.cfg1.cfg_from_ini(self.init_cfg_path)

        # just keep python script arg only, or it'll raise error while parsing..
        # ['python -m unittest', 'test.test_IO_Converter'] -> ['python -m unittest']
        sys.argv = [sys.argv[0]]
        argp_cfg = self.cfg_cnvter.cnvt_cfg_to(self.cfg1, 'argparse')
        self.assertIsInstance(argp_cfg, argparse.Namespace)
        # all section has been converted into dict
        self.assertIsInstance(argp_cfg.sec1, dict)
        self.assertIsInstance(argp_cfg.sec1['sec2'], dict)

        # convert easy_config instance into the "yaml string"
        yaml_cfg = self.cfg_cnvter.cnvt_cfg_to(self.cfg1, 'yaml')
        self.assertIsInstance(yaml_cfg, str)

        yaml_dict = yaml.load(yaml_cfg, Loader=yaml.FullLoader)
        self.assertIsInstance(yaml_dict, dict)

        ome_cfg = self.cfg_cnvter.cnvt_cfg_to(self.cfg1, 'omegaconf')
        self.assertIsInstance(ome_cfg, DictConfig)

        # there's no self.cfg_cnvter.cnvt_cfg_to(., 'dataclass')
        # since, namespace is not frequently used to intergrate with the other package..
        
    def test_convert_from(self):
        self.cfg1.cfg_from_ini(self.init_cfg_path)
        sys.argv = [sys.argv[0]]
        argp_cfg = self.cfg_cnvter.cnvt_cfg_to(self.cfg1, 'argparse')
        ez_cfg_argp = self.cfg_cnvter.cnvt_cfg_from(argp_cfg, 'argparse')
        self.assertIsInstance(ez_cfg_argp.sec1, AttributeDict)
        self.assertIsInstance(ez_cfg_argp.sec1.sec2, AttributeDict)

        yaml_cfg = self.cfg_cnvter.cnvt_cfg_to(self.cfg1, 'yaml')
        ez_cfg_yaml = self.cfg_cnvter.cnvt_cfg_from(yaml_cfg, 'yaml')
        self.assertIsInstance(ez_cfg_yaml.sec1, AttributeDict)
        self.assertIsInstance(ez_cfg_yaml.sec1.sec2, AttributeDict)

        ome_cfg = self.cfg_cnvter.cnvt_cfg_to(self.cfg1, 'omegaconf')
        ez_cfg_ome = self.cfg_cnvter.cnvt_cfg_from(ome_cfg, 'omegaconf')
        self.assertIsInstance(ez_cfg_ome.sec1, AttributeDict)
        self.assertIsInstance(ez_cfg_ome.sec1.sec2, AttributeDict)

        data_cls_cfg = ServerConfig()
        ez_cfg_dscls = self.cfg_cnvter.cnvt_cfg_from(data_cls_cfg, 'dataclass')
        self.assertIsInstance(ez_cfg_dscls.db, AttributeDict)
        self.assertIsInstance(ez_cfg_dscls.db.table_cfg, AttributeDict)

if __name__ == '__main__':
    tests = ['test_convert_to', 'test_convert_from']
    suite = unittest.TestSuite(map(IO_ConverterTestCase, tests))
    unittest.main(verbosity=2)