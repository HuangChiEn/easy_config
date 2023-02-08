from .Configer import Configer
from argparse import ArgumentParser

class IO_Convertor(object):
    def __init__(self):
        # support package regist :
        self.dispatcher = {
            'argparse' : self.argparse_cnvt,
        }

    def cnvt_cfg(self, cfg: Configer, target_cfg_type:str, **cnvtr_kwarg):
        assert target_cfg_type in self.dispatcher.keys(), '''Unfortunately, {} config is not supported yet\n
                                                Currently, easy_configer only support : {}'''.format(
                                                    target_cfg_type, self.dispatcher.keys()
                                            )

        return self.dispatcher[target_cfg_type](cfg, **cnvtr_kwarg)

    def argparse_cnvt(self, raw_cfg, parse_arg=True, flatten_args=True):
        args_template = ArgumentParser(description=raw_cfg._doc_str)
        cfg_gen = ( (k, v) for k, v in raw_cfg.__dict__.items() )
        for sec_key, sec_val in raw_cfg.__dict__.items():
            if flatten_args and isinstance(sec_val, dict):
                for key, val in sec_val.items():
                    args_template.add_argument(f"--{key}", type=type(val), default=val)
            else:
                args_template.add_argument(f"--{sec_key}", type=type(sec_val), default=sec_val)

        return args_template.parse_args() if parse_arg else args_template
