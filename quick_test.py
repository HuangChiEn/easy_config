from easy_configer.Configer import Configer

def build_cfg_text_a():
    return '''
    # Initial config file :
    inpo = 46@int
    > ./test/test_cfg_a.ini

    [test]         
        mrg_tst_var = [1, 3, 5]
        tst_var = ''@tst_cls
        [test.ggap]
            gtgt = $Section_test_A.tst_ext_var
    [ghyu]
        [ghyu.opop]
            add = 32
            [ghyu.opop.tueo]
                salt = $test.ggap.gtgt
        

    # Cell cfg written by Josef-Huang..
    '''

def build_cfg_text_b():
    return '''
    # Initial config file :
    inop = 32@int
    [test]         
        mrg_tst_var = [2, 4, 6]
        [test.ggap]
            gtgt = 'overrides'
            [test.ggap.conf]
                secert = 42

    [ghyu]
        [ghyu.opop]
            add = 67
            div = 1e-4

    [new]
        [new.new]
            newsec = wpeo@str 
            os_env = $ENV.test_env
            #    ? this variable is for testing the identical section name is whatever valid \
            #        for their nested section name

            inp_var = $ghyu.opop.add
            #    ? this variable is for testing the identical section name is whatever valid for their nested \
            #        section name and the intepolated variable could be show in here or not !!

    # Cell cfg written by Josef-Huang..
    '''

class Tst_cls:
    def __init__(self, kk=15, pp='josef'):
        self.kk = kk
        self.pp = pp
    
    def get_pp(self):
        return self.pp * 2

if __name__ == "__main__":
    from easy_configer.IO_Converter import IO_Converter

    from dataclasses import dataclass
    from typing import Optional

    @dataclass
    class TableConfig:
        rows: int = 1

    @dataclass
    class DatabaseConfig:
        table_cfg: TableConfig = TableConfig()

    @dataclass
    class ModelConfig:
        data_source: Optional[TableConfig] = None

    @dataclass
    class ServerConfig:
        db: DatabaseConfig
        model: ModelConfig


    cfg_a = Configer(cmd_args=False)
    cfg_a.regist_cnvtor("tst_cls", Tst_cls)  # regist customer class
    #cfg_a.cfg_from_cli()  
    cfg_a.cfg_from_str(build_cfg_text_a())
    #cfg_b = Configer()
    #cfg_b.cfg_from_str(build_cfg_text_b())

    #cfg_a.merge_conf(cfg_b, override=True)
    #cfg_b |= cfg_a

    breakpoint()
    #tmp = cfg_b + cfg_a
    
    # Note that you can use :
    #   python test.py test.mrg_var_tst "{'yeah':'success'}@dict" 
    #   to change the any default value in commend-line!!
    cnvt = IO_Converter()
    #tmp = cnvt.cnvt_cfg_to(cfg_b, 'yaml')

    ''' # test subgroup feature..
    from argparse import ArgumentParser
    parser = ArgumentParser(description='This is test!!')
    parser.add_argument("--pos1", default=42, help="positional argument 1")
    parser.add_argument("--pos2", default={'kk':42, 'aa':{'bb':44}}, help="positional argument 1")
    parser.add_argument("--pos3", default=False, help="positional argument 1")
    #args = parser.parse_args()
    '''

    tmp = cnvt.cnvt_cfg_to(cfg_b, 'omegaconf')
    print(f"convert to yaml-str : \n{tmp}\n\n")
    tst = cnvt.cnvt_cfg_from(tmp, 'omegaconf')
    print(tst)
    breakpoint()
    



# DEV TODO List:
# 1. rewrite exception for __get_declr_dict     ()
# 2. better flag syntax for cmdline support, refer to sweeper ~ ()