.. role:: raw-html-m2r(raw)
   :format: html


.. image:: assets/logo.png
   :target: assets/logo.png
   :alt: easy-configer logo


關於此專案
=====================

🚧 待完成任務 :
^^^^^^^^^^^^^^^^^^
#.
   釋出 v2.5.6 版中已知的問題，並 hot-fix 於 v2.6 版本群

#. 
   Tag v2.6 作為穩定版本

#.
   下一代 v3.0 版本處於開發中，將建構無狀態介面作為新的 features

#.
   支援套嵌型態的組態參數插值功能可能作為新的 features 釋出於 v3.0 版本

#. 
   您可以 preview v3.0 版本的程式碼雛形於 ./dev 資料夾底下 


🐞 已知問題 : 
^^^^^^^^^^^^^^^^^^^

#.
   allow_overwrite 旗標將允許您之後的單一組態值覆寫整個 section 的參數，這通常不會是使用者期望的行為 (pitfall)

#.
   無法用使用者命令列指定的參數更新 sub_config 中的組態值，這個設定當時被我寫死了 (bug)

----

前言 ✨
^^^^^^^^^

easy_configer 版本 : 2.5.6

用輕鬆的方法組態您的程式 

我很榮幸向使用者推出一個輕量化的組態工具作為配置python程式的設定，
希望這個工具能讓使用者輕鬆地控制大型專案 ~ ~

開發背景 📝
^^^^^^^^^^^^^^^

🙋‍♂️ 使用 easy_configer 的理由 ?
"""""""""""""""""""""""""""""""""

當走向大型專案的規模，我們會需要許多參數來控制程式的複雜業務邏輯；最終使用者可能需要一個簡單的解決方案來加載程式參數的組態。
雖然現今已經有許多套件提供這些功能，**不幸的是，我目前仍未看到一個完整的解決方案能夠輕鬆地加載和使用這些組態**；反之，大多套件都有自己的強項和短處，而他們的短處使得程式更加冗長和不易閱讀。

例如 :

.. code-block:: python

   ## ConfigParser
   import ConfigParser 
   Config = ConfigParser.ConfigParser()
   Config.read("c:\\tomorrow.ini")
   # get arg via method
   Config.get(section, option)
   # or get arg with converter
   int(Config['lucky_num'])

   ## Argparse
   import argparse
   parse = argparse.ArgumentParser("description string")
   parse.add_argument("--lucky_num", type=int)
   ...
   args = parser.parse_args()
   args.lucky_num

   ## Omegaconf
   from omegaconf import OmegaConf
   conf = OmegaConf.load('source/example.yaml')
   conf.player.height


除了 omegaconf，許多配置工具在載入和訪問配置參數時有很多冗餘的語法。
然而，omegaconf 本身也有幾個缺點：

#. 
   依賴性太多（版本兼容性可能會成為問題！）

#. 
   動態配置加載系統難以追蹤（是哪些配置覆蓋了我的默認設置？）

#. 
   非原生容器（它應用了 Mappable 物件，因此需要使用 to_container 進行進一步轉換）

這促使我打包了解決這些問題的方案，與之相對的 easy_configer 具有對應的優點：

#. 
   沒有依賴套件！！（除非你想將 easy_configer 轉換為其他配置工具的實例）

#. 
   靈活應用 :code:`allow_overwrite=False`，你可以輕鬆檢測到被覆蓋的參數。

#. 
   我們的容器繼承自純 Python 字典！大多數字典方法也可以正常使用。

easy_configer 解決方案也將包括以下特性：

#. 
   **階層性組態 (多層次的字典結構)**

#. 
   **接受多個配置文件並支持動態加載 (類似於omegaconf)**

#. 
   **支援自定義的資料型態 (藉由 list 或 keyword 參數初始化您的類別)**

#. 
   **可於命令列中 新增/更新 任意組態值 (即使組態位於section)**

#. 
   **支援 absl 風格的 FLAGS 功能 (定義一次、用於所有地方)** 

當然，解決方案也支援以下功能：

* 
  對於任何參數，可使用 dot 運算子訪問 (即使是內嵌字典的參數)

* 
  內聯註釋 "#"，現在您可以在每一行中寫註釋了

* 
  支援參數插值 (即使參數位於內嵌字典)!

* 
  支援組態檔轉換，將 easy_config 轉換到不同組態套件 (omegaconf, argparse, ..., 等第三方套件)

* 
  支援具有動態載入的多層次配置系統 ~
