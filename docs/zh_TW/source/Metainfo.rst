.. role:: raw-html-m2r(raw)
   :format: html

套件相關資訊
=============

新增功能 🚀
^^^^^^^^^^^^^

#. 
  v2.5.4 基本上堪用，但仍有一些 known issues (撰寫於 關於此專案中)，因此我計畫釋出 v2.6 版本作為重大更新前的穩定版本

#. 
   使用 ${cfg}, ${env} 來分別啟用參數插值、環境變數導入的功能

#. 
   使用 AttributeDict 作為內嵌組態的容器 (它直接繼承python dict物件)

----


修正的Bug 🐛
^^^^^^^^^^^^^^

Hot-fix AttributeDict 不會 raise NoAttributeError 的錯誤,
Hot-fix 組態覆寫的bug, 並提供參數設定是否進行組態覆寫..

----

簡易 Unittest 🧪
^^^^^^^^^^^^^^^^^^

如果您從 github 克隆此專案，你可以嘗試運行下面的測試指令。
``python -m unittest discover``

..

   我將所有測試案例置放於 test 資料夾底下。

----

其餘資訊 🦠 
^^^^^^^^^^^^

License
MIT License. 關於條款細項請參閱 LICENSE.md

開發者
Josef-Huang, a3285556aa@gmail.com 

尾頁
Hope God bless everyone in the world to know his word ~ :raw-html-m2r:`<br>`
**敬畏耶和華是智慧的開端，認識至聖者便是聰明。 箴言九章十節**
