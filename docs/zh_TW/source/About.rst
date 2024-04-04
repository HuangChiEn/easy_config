.. role:: raw-html-m2r(raw)
   :format: html


.. image:: assets/logo.png
   :target: assets/logo.png
   :alt: easy-configer logo


關於此專案
=====================

前言 ✨
^^^^^^^^^

easy_configer 版本 : 2.3.2

..

   小提示 :  2.3.1 版只是對 pypi 上文檔的修正

用輕鬆的方法組態您的程式 

我很榮幸向使用者推出一個輕量化的組態工具作為配置python程式的設定，
希望這個工具能讓使用者輕鬆地控制大型專案 ~ ~

開發背景 📝
^^^^^^^^^^^^^^^

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



這促使我提出一個新的解決方案來應對這些問題。easy_configer 將包括以下特性：

#. 
   **階層性組態 (多層次的字典結構)**

#. 
   **接受多個配置文件並支持動態加載**

#. 
   **支援自定義的資料型態 (藉由 keyword 參數初始化您的類別)**

#. 
   **可於命令列中更新任意組態值，不論其所屬階層與位置**

#. 
   **支援 absl 風格的 FLAGS 功能** 

當然，解決方案也支援以下功能：

* 
  對於任何參數，可使用 dot 運算子訪問 (即使是字典中字典的參數)

* 
  內聯註釋 "#"，現在您可以在每一行中寫註釋了

* 
  支援參數插值!!

* 
  支援組態檔轉換，將 easy_config 轉換到不同組態套件 (omegaconf, argparse, ..., 等第三方套件)

* 
  支援具有動態覆蓋的多層次配置系統 ~
