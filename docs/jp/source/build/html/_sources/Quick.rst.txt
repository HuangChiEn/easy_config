.. role:: raw-html-m2r(raw)
   :format: html


クイックスタート
==================

設定ファイルの素早い導入例 🥂
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Jupyter Notebook で開発環境用の easy_config を使用しているとします。
簡単な数学計算を構成するためにいくつかの変数を定義したいとします。

.. code-block:: python

   # config string
   cfg_str = '''
   title = 'math calculation'@str
   coef = 1e-3@float
   with_intercept = True@bool
   intercept = 3@int
   '''

   # looks great, let us get the config!
   from easy_configer.Configer import Configer
   cfg = Configer(description="math calculation config!", cmd_args=False)
   cfg.cfg_from_str(cfg_str)

   # oh.. wait, could we do it more easier ?
   ez_cfg_str = '''
   # opps.. let's change some value
   title = 'linear equation'
   coef = 15        
   '''
   # Note : every time you load the config, if you have the same variable name,
   #        it will override the value of the variable!
   cfg.cfg_from_str(ez_cfg_str)

   lin_equ = lambda x : cfg.coef * x + cfg.intercept if cfg.with_intercept else (cfg.coef * x)
   x = 15
   print( f"Linear equation with x={x} : { lin_equ(x) }" )

..

    もし以前の設定を上書きしたい場合、``cfg.cfg_from_str`` を ``allow_overwrite=True`` フラグで2回適用する方法は推奨されません。
    easy-configerでは、これを行う方法を2つ提供しています。標準的な方法は、2つの設定を宣言し、設定のマージ方法を適用して更新された設定を取得することです。
    もう一つの方法は、omegaconfのように動的にサブ設定をインポートする方法ですが、 ``cfg.cfg_from_ini`` で ``allow_overwrite=True`` フラグを設定する必要があります。

Pythonで文字列設定を記述することは便利ですが、これは小規模なプロジェクトにのみ適しています。
より大規模なプロジェクトでは、プログラムを制御するために設定ファイルを作成し、設定を追跡し、確認し、デバッグしやすくすることが一般的です。ここでは、まず、作業ディレクトリに ``test_cfg.ini`` という名前の設定ファイルを用意し、チャットボットとどのように連携するかを大まかに説明します。

easy-configer では、設定ファイルに2種類の引数があります：フラットな引数と階層的な引数です。
フラットな引数は、設定内で直接配置され、特定のセクションに属さない（つまり、最初のレベルに配置されます）。
一方、階層的な引数は、セクション（例： ``[db_setup]`` ）に配置され、任意の深さを持つことができます。
セクション内の引数は、純粋な Python の dict に似たコンテナ（ ``easy_configer.utils.Container.AttributeDict`` ）にラップされます。

階層的な引数をネストされたセクションで形成するために、toml のような構文を使用してネストされたセクションを記述します（例： ``[bknd_srv.mod_params]`` は ``[bknd_srv]`` の親セクションに属します）。
ネストされたセクション内の引数も、ネストされた ``AttributeDict`` にラップされます。さらに、ドット演算子を使ってすべての引数にアクセスできますが、純粋な Python の辞書のようにキー文字列を使用することをお勧めします。

..

    なお、引数にアクセスする推奨される方法は、依然として キー文字列アクセス ``cfger.args['#4$%-var']`` です。
    ご覧のように、ドットアクセスは **不格好な変数名** （ ``cfger.#4$%-var`` ）をサポートしていません（変数名は Python インタプリタでは無効です）。

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
       db_host = ${cfg.serv_host}:80@str
       # first `export mongo_port=5566` in your bash, then support os.env interpolation!
       db_port = ${env.mongo_port}   
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
           model_mode = ${cfg.bknd_srv.chat_mode}  # hierachical args interpolation


:raw-html-m2r:`<br>`

現在、工作ディレクトリで ``python quick_start.py`` を実行することでチャットボットを起動できます (\ *quick_start.py はあなたの作業ディレクトリにあります*\ )!
もちろん、コマンドラインから  ``python quick_start.py serv_port=7894`` を使用してパラメータ設定を上書きすることもできます。

..

    なお、コマンドラインからの引数の更新は自然に許可されていますが、セクションの上書きは許可されていません！
    セクションを上書きしたい場合は、 ``allow_overwrite=True`` フラグを設定する必要があります。

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
       # you can access nested-dict by dot access ~
       llm_mod.init_mod_param( **cfger.bknd_srv.mod_params )

       # or you can keep the dict fashion ~
       if cfger.bknd_srv['async_req']:
           chat_serv.chat_mod = llm_mod
           chat_serv.hist_db = mongo_serv
       else:
           ... # write sync conversation by yourself..

       sys.exit( chat_serv.server_forever() )


:raw-html-m2r:`<br>`

*次の章では、より詳細なチュートリアルを提供します。*
