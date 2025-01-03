.. role:: raw-html-m2r(raw)
   :format: html


Quick start 
============

Handy example of config file 🥂
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's say we have an easy-config for development enviroment on jupyter notebook. we want to define several variable for configurating a simple math calculation.

.. code-block:: python

   # config string
   cfg_str = '''
   title = 'math calculation'@str
   coef = 1e-3@float
   with_intercept = True@bool
   intercept = 3@int
   '''

   # look's good, let's get the config!
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

    If you want to overwrite previous config, *apply twice* ``cfg.cfg_from_str`` with ``allow_overwrite=True`` flag IS NOT a recommended way. 
    In easy-configer, we provide 2 way to do that. The standard way is *declaring 2 config and apply config merging method* to get the updated config. 
    The other way is similar with omegaconf to import sub-config in dynamic manner,  however you still need to set flag ``allow_overwrite=True`` in ``cfg.cfg_from_ini``.

Although writing a string config in python is convenient, it only suitable for the project in smaller scale. 
In large project, we may write a config file to control the program, so that we will be easy to trace, check and debug the config. 
We are going to prepare a sample config called ``test_cfg.ini`` in the working directory and describe how we work with chatbot roughly. 

In easy-configer, there're two type of argument in config : flatten argument, hierachical argument. 
You will see that the flatten arguments are directly placed in config and doesn't belong any section (namely in first level). 
In contrast, the hierachical arguments will be placed in section (i.e. ``[db_setup]``) with any kind of depth, 
the arguments under the section will be wrapped by a container (`easy_configer.utils.Container.AttributeDict`) similar with pure python ``dict``. 

To form a hierachical argument in nested section, we apply toml-like syntax to describe the nested section (i.e. ``[bknd_srv.mod_params]`` is belong to ``[bknd_srv]`` parent section). 
The arguments in nested section are also wrapped by nested AttributeDict. Besides you can access all kind of arguments by the simple dot-operator, however, we still recommend you to use key-string as pure python dict.

..
    
    Note that the recommended way to access the argument is **still** key-string access ``cfger.args['#4$%-var']``, as you may notice, 
    dot-access doesn't support **ugly** variable name (``cfger.#4$%-var``, as variable name is invalid in python intepreter). 

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

Now, we're free to launch the chatbot via ``python quick_start.py`` (\ *quick_start.py in work directory*\ )!
However, you can also override the arguemnts via commendline ``python quick_start.py serv_port=7894``

..

    Note that **update argument** from commendline is naturally permitted, but overwrite **the section** IS NOT! 
    If you also want to overwrite the section, you need to set flag ``allow_overwrite=True``. 

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

*More detail tutorial is in the following chapter..*
