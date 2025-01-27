from argparse import ArgumentParser

# previous version dependecy..
from easy_configer.utils.Container import AttributeDict

class IO_Converter(object):
    '''
    The interface to convert easy_config instance to 'other common config' instance, and vice versa.
    Note : 
        the converted results may be slightly different according to the support of target config.
        For example, argparse doesn't explicitly provide a way for storing hierachical config, so the converted 
        config will be flattened! 
    '''
    def __init__(self):
        '''
        Constructor of converter. In here, we declare the output/input dispatcher to 
        dispatch the easy_config instance into the indicated subroutine.
        '''
        # 'o'utput to different config 
        self.output_dispatcher = {
            'argparse' : self._to_argparse,
            'omegaconf' : self._to_omegacfg,
            'yaml' : self._to_yaml,
            'dict' : self._to_dict
        }
        # 'i'nput from different config  
        self.input_dispatcher = {
            'argparse' : self._from_argparse,
            'omegaconf' : self._from_omegacfg,
            'yaml' : self._from_yaml,
            'dataclass' : self._from_dataclass,
            'dict' : self._from_dict
        }

    def cnvt_cfg_to(self, cfg, target_cfg_type:str, **cnvtr_kwarg):
        '''
        Convert easy_configer 'to' the other common config instance.

        Args:
            cfg (Configer): Easy_configer instance.
            target_cfg_type (str): A string tag of supported config type. It could be viewed by `self.output_dispatcher.keys()`.
            cnvtr_kwarg (`**kwargs`): Other keyword arguments attempt to pass to converter subroutine.

        Return:
            Any, the target config instance.
        '''
        assert target_cfg_type in self.output_dispatcher.keys(), '''Unfortunately, {0} config is not supported yet\n
                                                Currently, easy_configer only support : {1}'''.format(
                                                    target_cfg_type, self.output_dispatcher.keys()
                                            )
        return self.output_dispatcher[target_cfg_type](cfg, **cnvtr_kwarg)

    def cnvt_cfg_from(self, other_cfg, target_cfg_type:str, **cnvtr_kwarg):
        '''
        Convert to easy_configer 'from' the given common config instance.

        Args:
            other_cfg (Any): Any supported config instance. 
            target_cfg_type (str): A string tag of supported config type. It could be viewed by `self.input_dispatcher.keys()`.
            cnvtr_kwarg (`**kwargs`): Other keyword arguments attempt to pass to converter subroutine.

        Return:
            Configer.
        '''
        assert target_cfg_type in self.input_dispatcher.keys(), '''Unfortunately, {0} config is not supported yet\n
                                                Currently, easy_configer only support : {1}'''.format(
                                                    target_cfg_type, self.output_dispatcher.keys()
                                            )
        return self.input_dispatcher[target_cfg_type](other_cfg, **cnvtr_kwarg)

    # utils functions
    def __imp_pkg(self, pkg_path):
        ''' Utility function to import the corresponding config package. '''
        pypi_name = {
            'yaml' : 'pyyaml',
            'omegaconf' : 'omegaconf',
            'dataclasses' : 'dataclasses'
        }
        try:
            import importlib
            mod = importlib.import_module(pkg_path)
        except:
            pkg_name = pkg_path.split('.')[0]
            raise ImportError("Python version you used doesn't support native {0} pkg, " \
                            "please 'pip install {0}'.".format( pypi_name[pkg_name] ))
        return mod

    def __remove_private_var(self, raw_cfg):
        ''' 
        Shadow the private arguments before conversion. 
        Only used while convert easy_config to the other one. 
        '''
        tmp_dict = {}
        for k, v in raw_cfg.items():
            # all private attribute is presented at first level
            if not k.startswith('_'):
                tmp_dict[k] = v
        return tmp_dict

    def __convert_to_dict(self, sec_val):
        dct = {}
        for k, v in sec_val.items():
            if isinstance(v, AttributeDict):
                v = self.__convert_to_dict(v)
            dct[k] = v
        return dct
    
    def _to_dict(self, raw_cfg, return_attr_dict=False):
        cfg = self.__remove_private_var(raw_cfg)
        # force to convert AttributeDict into native python dict!
        return cfg if return_attr_dict else self.__convert_to_dict(cfg)

    # Convert easy_config to different config, QQ.. Byebye user..
    def _to_argparse(self, raw_cfg, parse_arg=True):
        args_template = ArgumentParser( description=raw_cfg.get_doc_str() )
        for sec_key, sec_val in self._to_dict(raw_cfg).items():         
            args_template.add_argument("--{0}".format(sec_key), type=type(sec_val), default=sec_val)
        
        return args_template.parse_args() if parse_arg else args_template

    def _to_yaml(self, raw_cfg):
        mod = self.__imp_pkg('yaml')
        cfg_dict = self._to_dict(raw_cfg)

        return mod.dump(cfg_dict)

    def _to_omegacfg(self, raw_cfg):
        mod = self.__imp_pkg('omegaconf.omegaconf')
        cfg_dict = self._to_dict(raw_cfg)
        return mod.OmegaConf.create(cfg_dict)
    
    # Convert different config to easy_config! welcome aboard, User ~ www
    def _from_argparse(self, arg_cfg):
        arg_cfg_dict = vars(arg_cfg)
        return self._from_dict(arg_cfg_dict)

    def _from_yaml(self, yaml_str):
        mod = self.__imp_pkg('yaml')
        yaml_dict = mod.safe_load(yaml_str)
        return self._from_dict(yaml_dict)

    def _from_omegacfg(self, omg_cfg):
        mod = self.__imp_pkg('omegaconf.omegaconf')
        omg_dict = mod.OmegaConf.to_container(omg_cfg)
        return self._from_dict(omg_dict)

    def _from_dataclass(self, datacls_cfg):
        mod = self.__imp_pkg('dataclasses')
        datacls_dict = mod.asdict(datacls_cfg)
        return self._from_dict(datacls_dict)

    def _from_dict(self, cfg_dict):
        from .dev_Configer import Configer
        cfg = Configer()
        for k, v in cfg_dict.items():
            if isinstance(v, dict):
                # set_attr_dict is enabled in init..
                # no need to convert the nested-dict manuelly!
                v = AttributeDict(v)
            cfg.__dict__[k] = v
        return cfg