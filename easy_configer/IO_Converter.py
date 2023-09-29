from .Configer import Configer
from argparse import ArgumentParser

class IO_Converter(object):
    def __init__(self):
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
            'dict' : self._from_dict
        }

    def cnvt_cfg_to(self, cfg: Configer, target_cfg_type:str, **cnvtr_kwarg):
        assert target_cfg_type in self.output_dispatcher.keys(), '''Unfortunately, {0} config is not supported yet\n
                                                Currently, easy_configer only support : {1}'''.format(
                                                    target_cfg_type, self.output_dispatcher.keys()
                                            )
        return self.output_dispatcher[target_cfg_type](cfg, **cnvtr_kwarg)

    def cnvt_cfg_from(self, other_cfg, target_cfg_type:str, **cnvtr_kwarg):
        assert target_cfg_type in self.input_dispatcher.keys(), '''Unfortunately, {0} config is not supported yet\n
                                                Currently, easy_configer only support : {1}'''.format(
                                                    target_cfg_type, self.output_dispatcher.keys()
                                            )
        return self.input_dispatcher[target_cfg_type](other_cfg, **cnvtr_kwarg)

    # utils functions
    def __imp_pkg(self, pkg_path):
        pypi_name = {
            'yaml' : 'pyyaml',
            'omegaconf' : 'omegaconf'
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
        tmp_dict = {}
        for k, v in raw_cfg.__dict__.items():
            if not k[0] == '_':
                tmp_dict[k] = v
        return tmp_dict

    # Convert easy_config to different config, QQ.. Byebye user..
    def _to_argparse(self, raw_cfg, parse_arg=True, flatten_args=True):
        args_template = ArgumentParser( description=raw_cfg.get_doc_str() )
        raw_dict = self.__remove_private_var(raw_cfg)
        
        for sec_key, sec_val in raw_dict.items():
            if flatten_args and isinstance(sec_val, dict):
                for key, val in sec_val.items():
                    args_template.add_argument("--{0}".format(key), type=type(val), default=val)
            else:
                args_template.add_argument("--{0}".format(sec_key), type=type(sec_val), default=sec_val)

        return args_template.parse_args() if parse_arg else args_template

    def _to_yaml(self, raw_cfg):
        mod = self.__imp_pkg('yaml')
        raw_dict = self.__remove_private_var(raw_cfg)
        return mod.dump(raw_dict)

    def _to_omegacfg(self, raw_cfg):
        mod = self.__imp_pkg('omegaconf.omegaconf')
        raw_dict = self.__remove_private_var(raw_cfg)
        return mod.OmegaConf.create(raw_dict)

    def _to_dict(self, raw_cfg):
        return self.__remove_private_var(raw_cfg)
    
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

    def _from_dict(self, cfg_dict):
        cfg = Configer()
        for k, v in cfg_dict.items():
            cfg.__dict__[k] = v
        return cfg