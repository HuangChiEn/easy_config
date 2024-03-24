class Customized_Object(object):
    
    def __init__(self, arg1=None, arg2=None, *lst_args, **kw_args):
        self.arg1 = arg1
        self.arg2 = arg2
        self.lst_args = lst_args
        self.kw_args = kw_args
    
    def get_args(self):
        return (self.arg1, self.arg2)
    
    def get_lst_args(self):
        return self.lst_args

    def get_kw_args(self):
        return self.kw_args


def get_cfg_str(cfg_path):
    with open(cfg_path, 'r') as f_ptr:
        cfg_str = f_ptr.read()
    return cfg_str