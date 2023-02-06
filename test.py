
from easy_config.Configer import Configer

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
    cfg = Configer()
    cfg.cfg_from_ini("./test/test_cfg.ini")
    print(cfg)

    breakpoint()

