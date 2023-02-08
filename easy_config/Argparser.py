import sys

class Argparser:

    # Update the namespace value via commend-line input 
    @staticmethod
    def args_from_cmd(cfg_dict):

        def is_long_flag(flag_str):
            prefix = flag_str[0:2]
            return True if prefix == "--" else False
            
        '''
            Update the arguments by commend line input string
        '''
        # remove file name from args
        cmd_arg_lst = sys.argv[1:]

        # print out helper document string
        if "-h" in cmd_arg_lst:
            cmd_arg_lst.remove("-h")
            print(cfg_dict['_doc_str'])

        for idx, item in enumerate(cmd_arg_lst):
            if idx % 2 == 0:  # argument flag 
                if is_long_flag(item):
                    flag = item[2:]
                    flag_lst = flag.split('-')
                    sec_key, arg = flag_lst[0], flag_lst[1]
                else:
                    arg = item[1:]
                    sec_key = ""
                    
            else:     # argument value 
                val = item
                if sec_key == "":
                    cfg_dict[arg] = val
                else:
                    cfg_dict[sec_key][arg] = val
