.. role:: raw-html-m2r(raw)
   :format: html


快速入門
==========

撰寫 config file 的快速上手範例 🥂
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

讓我們假設在 Jupyter Notebook 中有一個用於開發環境的 easy_config。我們想要定義一些變量來配置一個簡單的數學計算。

.. code-block:: python

   # config 字串
   cfg_str = '''
   title = 'math calculation'@str
   coef = 1e-3@float
   with_intercept = True@bool
   intercept = 3@int
   '''

   # 看起來不錯, 讓我們取得 config!
   from easy_configer.Config import Config
   cfg = Config(description="math calculation config!", cmd_args=False)
   cfg.cfg_from_str(cfg_str)

   # 喔.. 且慢, 我們可以讓它變得更簡單嗎 ?
   ez_cfg_str = '''
   # opps.. let's change some value
   title = 'linear equation'
   coef = 15        
   '''
   # 請留意 : 每次我們加載 config, 具有同樣變數名稱的參數將被新加載的 config 複寫!!
   cfg.cfg_from_str(ez_cfg_str)

   lin_equ = lambda x : cfg.coef * x + cfg.intercept if cfg.with_intercept else (cfg.coef * x)
   x = 15
   print( f"Linear equation with x={x} : { lin_equ(x) }" )



在較大型的項目中，我們可能會編寫一個配置文件來控制程序，使得配置更容易追蹤、檢查和調試。在這裡，我們首先在工作目錄中準備一個名為 ``test_cfg.ini`` 的配置文件。
*對於 easy-config 文件，存在兩種類型的參數：扁平參數和層次參數*。您可以看到，扁平參數位於第一層級，可以通過點運算符輕鬆訪問；除了扁平參數之外，所有層次參數將被放置在 Python 字典對象中，因此可以通過字串訪問每個參數！

.. code-block:: ini

   # ./test_cfg.ini
   # '#' denote comment line, the inline comment is also supported!

   # define 'flatten' arguments :
   serv_host = '127.0.0.1'  
   serv_port = 9478@int    # specific type is also allowed!!
   api_keys = {'TW_REGION':'SV92VS92N20', 'US_REGION':'W92N8WN029N2'}

   # define 'hierachical' arguments :
   # the 'section' is the key of accessing dict value and could be defined as follows :
   [db_setup]
       db_host = $serv_host
       # first `export mongo_port=5566` in your bash, then support os.env interpolation!
       db_port = $Env.mongo_port  
       snap_shot = True

   # and then define second section for backend server..
   [bknd_srv]
       load_8bit = True
       async_req = True
       chat_mode = 'inference'
       model_type = 'LlaMa2.0'
       [bknd_srv.mod_params]
           log_hist = False
           tempeture = 1e-4
           model_mode = $bknd_srv.chat_mode  # hierachical args interpolation


:raw-html-m2r:`<br>`

現在，您可以通過在工作目錄中運行 ``python quick_start.py`` 來啟動聊天機器人 (\ *quick_start.py 在您的工作目錄中*\ )!
當然，您也可以通過命令行使用 ``python quick_start.py serv_port=7894`` 來覆蓋參數設置。

.. code-block:: python

   import sys

   # main_block 
   if __name__ == "__main__":
       from easy_configer.Configer import Configer

       cfger = Configer(description="chat-bot configuration", cmd_args=True)
       # we have defined a config file, let's try to load it!
       cfger.cfg_from_ini("./test_cfg.ini")

       # Display the Namespace, it will display all flatten arguemnts and first-level sections
       print(cfger)

       ... # for building chat-bot instance `Chat_server`
       chat_serv = Chat_server(host=cfger.serv_host, port=cfger.serv_port, api_keys=cfger.api_keys)

       ... # build mongo-db instance `mongo_serv` for logging chat history..
       mongo_serv.init_setup( **cfger.db_setup )

       ... # loading llm model instance `Llama` ~
       llm_mod = Llama(
           ld_8bit=cfger.bknd_srv.load_8bit, 
           chat_mode=cfger.chat_mode, 
           model_type=cfger.model_type
       )
       llm_mod.init_mod_param( **cfger.bknd_srv['mod_params'] )

       if cfger.bknd_srv['async_req']:
           chat_serv.chat_mod = llm_mod
           chat_serv.hist_db = mongo_serv
       else:
           ... # write sync conversation by yourself..

       sys.exit( chat_serv.server_forever() )


:raw-html-m2r:`<br>`

*在接下來的章節中，將提供更詳細的教學...*
