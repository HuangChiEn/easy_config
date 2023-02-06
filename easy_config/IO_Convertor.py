from .Configer import Configer
from argparse import ArgumentParser

# support package regist :
# TODO list : support omegaconf
 = [
    'argparse', 
]

class IO_Convertor(object):
    def __init__(self):
        self.dispatcher = {
            'argparse' : self.argparse_cnvt,
        }

    def cnvt_cfg(cfg: Configer, target_cfg_type:str):
        assert target_typ in self.dispatcher.keys(), '''Unfortunately, {} config is not supported yet\n
                                                Currently, easy_configer only support : {}'''.format(
                                                    target_cfg_type, self.dispatcher.keys()
                                            )

        return self.dispatcher[target_cfg_type](cfg)

    def argparse_cnvt(self, raw_cfg):
        args_template = ArgumentParser(description=raw_cfg.doc_str)
        cfg_gen = ( (k, v) for k, v in raw_cfg.__dict__.items() if isinstance(v, dict))
        for k, v in cfg_gen:
            for key, val in getattr(cfger, k).items():
                setattr(args_template, key, val)

        return args_template
