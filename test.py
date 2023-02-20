from easy_configer.Configer import Configer

def _build_cfg_text():
    return '''
    # Initial config file :
    [test]         
    mrg_var_tst = [1, 3, 5]@list

    [Section_test_B]
    fflg = False@bool   # test inline comment in cfg-str
    tflg = True@bool
    # Cell cfg written by Josef-Huang..
    '''

if __name__ == "__main__":
    cfg = Configer()
    cfg.cfg_from_str(_build_cfg_text())
    breakpoint()