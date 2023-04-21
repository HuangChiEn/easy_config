from .Configer import Configer

from argparse import ArgumentParser
from omegaconf import OmegaConf
import yaml

class IO_Converter(object):
    def __init__(self):
        # support package regist :
        self.dispatcher = {
            'argparse' : self.argparse_cnvt,
            'omegacfg' : self.omegacfg_cvnt,
            'yaml' : self.yaml_cnvt
        }

    def __remove_private_var(self, raw_cfg):
        tmp_dict = {}
        for k, v in raw_cfg.__dict__.items():
            if not k[0] == '_':
                tmp_dict[k] = v
        return tmp_dict

    def cnvt_cfg(self, cfg: Configer, target_cfg_type:str, **cnvtr_kwarg):
        assert target_cfg_type in self.dispatcher.keys(), '''Unfortunately, {} config is not supported yet\n
                                                Currently, easy_configer only support : {}'''.format(
                                                    target_cfg_type, self.dispatcher.keys()
                                            )
        return self.dispatcher[target_cfg_type](cfg, **cnvtr_kwarg)

    def argparse_cnvt(self, raw_cfg, parse_arg=True, flatten_args=True):
        args_template = ArgumentParser( description=raw_cfg.get_doc_str() )
        raw_dict = self.__remove_private_var(raw_cfg)
        
        for sec_key, sec_val in raw_dict.items():
            if flatten_args and isinstance(sec_val, dict):
                for key, val in sec_val.items():
                    args_template.add_argument(f"--{key}", type=type(val), default=val)
            else:
                args_template.add_argument(f"--{sec_key}", type=type(sec_val), default=sec_val)

        return args_template.parse_args() if parse_arg else args_template

    def yaml_cnvt(self, raw_cfg):
        raw_dict = self.__remove_private_var(raw_cfg)
        return yaml.dump(raw_dict)

    def omegacfg_cvnt(self, raw_cfg):
        raw_dict = self.__remove_private_var(raw_cfg)
        return OmegaConf.create(raw_dict)
        