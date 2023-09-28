import sys
from .utils.Type_Convertor import Type_Convertor

class Argparser:

    # Update the namespace value via commend-line input 
    @staticmethod
    def args_from_cmd(idx_sec_by_dot):   
        '''
            Update the arguments by commend line input string
        '''
        # Note that argument key should begin with - symbol for increasing read-ability!
        def is_arg_key(cmd_str):
            if cmd_str[0] == '-':
                return True
            else:
                return False

        typ_cnvt = Type_Convertor()

        # remove file name from args
        cmd_arg_lst = sys.argv[1:]
        
        # print out helper document string
        if "-h" in cmd_arg_lst:
            cmd_arg_lst.remove("-h")
            print(cfg_dict['_doc_str'])

        sec_ptr, sec_key = None, None
        for idx, item in enumerate(cmd_arg_lst):
            if is_arg_key(item):  # argument flag 
                sec_keys_str = item.split('-')[-1]   # strip - symbol, and get argument key
                sec_ptr, sec_key = idx_sec_by_dot(sec_keys_str, allow_init=True)       
            else:                # argument value 
                if idx % 2 == 0:
                    raise RuntimeError('Commendline argument missing the argument key, note that argument key should begin with - symbol!')
                val_str = item
                sec_ptr[sec_key] = typ_cnvt.convert(val_str)
                