
from easy_config.Configer import Configer
from easy_config.IO_Convertor import IO_Convertor

'''
new features of easy_configer string, parse toml like format!!
[servers]
  support sub-struct of cfg
  # Indentation (tabs and/or spaces) is allowed but not required
  [servers.alpha]
  ip = "10.0.0.1"
  dc = "eqdc10"
'''


if __name__ == "__main__":
    cfg = Configer("hello LW cfg", cmd_args=True)
    cfg.cfg_from_ini("./test/test_cfg.ini")
    print(cfg)

    breakpoint()
    io_cnvt = IO_Convertor()
    tmp = io_cnvt.cnvt_cfg(cfg, 'argparse', parse_arg=False)

    breakpoint()
    io_cnvt = IO_Convertor()
    tmp = io_cnvt.cnvt_cfg(cfg, 'argparse', parse_arg=False)

