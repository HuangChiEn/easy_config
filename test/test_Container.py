import unittest
import unittest.mock

from easy_configer.utils.Container import AttributeDict

class ConfigerTestCase(unittest.TestCase):
    
    def setUp(self):
        self.attr_dct = None
    
    def _get_hier_dct(self):
        return {
            # str & int as key
            'var' : 42,
            # shallow nested dict
            'dct' : {
                'var' : 42,
            }
        }
    
    def test_dict_methods(self):
        self.attr_dct = AttributeDict(init_dict=self._get_hier_dct())

        self.assertIsInstance(self.attr_dct, AttributeDict)
        self.assertIsInstance(self.attr_dct['dct'], AttributeDict)
        self.assertTrue( issubclass(AttributeDict, dict) )

        # ? basically, attribute dict should act as same as dict
        hier_dct = self._get_hier_dct()
        self.assertEqual(self.attr_dct['var'], hier_dct['var'])

        # * basic method of dict
        self.assertEqual(self.attr_dct.get('var_not_declared', -1), hier_dct.get('var_not_declared', -1))
        self.assertEqual(self.attr_dct['dct'].get('var', -1), hier_dct['dct'].get('var', -1))

        self.assertEqual(self.attr_dct.keys(), hier_dct.keys())
        self.assertEqual(self.attr_dct.items(), hier_dct.items())
        
        val1, val2 = [ v for v in self.attr_dct.values() ], [ v for v in hier_dct.values() ]
        self.assertEqual(val1, val2)
        


if __name__ == '__main__':
    tests = ['test_dict_methods']
    suite = unittest.TestSuite(map(ConfigerTestCase, tests))
    unittest.main(verbosity=2)