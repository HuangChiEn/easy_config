.. role:: raw-html-m2r(raw)
   :format: html

下載教學
=============


如何下載 ? ⚙️\ :raw-html-m2r:`<br>`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. **透過 pypi 下載** :raw-html-m2r:`<br>`
    簡易的輸入 ``pip install easy_configer`` 指令於您的命令提示字元 (因為套件名稱衝突，在pypi是使用不同的套件名稱)
#. **透過原始碼下載** :raw-html-m2r:`<br>`
    從 github 克隆專案至本地端 : ``git clone repo-link`` 
    切換到克隆專案的根目錄，並輸入 ``pip install -e .``
#. **import 語法** :raw-html-m2r:`<br>`
    由於 pypi 套件的名稱出同，採用了不同的套件名稱。
    因此在 import 下載的套件時，使用的語法將視您的下載方式而定。例如: :raw-html-m2r:`<br>`
    透過 pip 下載 : ``from easy_configer.Configer import Configer`` :raw-html-m2r:`<br>`
    git 克隆 & pip 下載 : ``from easy_config.Configer import Configer`` :raw-html-m2r:`<br>`

----

套件相依性 🏗️
^^^^^^^^^^^^^^^^^^

此套件最初為 Python 3.8 撰寫，經測試可運行於 3.6+ 版本。理所當然，輕量化的解決方案 **不相依於** 任何三方套件。
我只使用 python 標準函式庫的套件 (例如 pathlib, sys, ... 等等)，因此您無需擔心任何套件相依問題 ~ ~

..

   然而，如果您有使用到 IO_Converter 功能來轉換組態物件到其他套件 (例如, omegaconf)，您還是需要下載 omegaconf 套件，並留意相關版本 ~
