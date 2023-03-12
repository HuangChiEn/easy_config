### Newly update features 🚀
1. I have took sometime to accept the truth those famous config-tools have the support from their community and eco-system. For example, torchlightning's Trainer take argparse as input; fb hydra take omegaconf as input. **So, easy_configer now provide a converter mechnaism allowing user convert our easy_config into the other famous config-tools (s.t. argparse, omegaconf, and yaml).**  

2. There's an common usage case that the pre-defined arguments may be reused in the other section. So, we also support the argument interpolation. However, the **shared arguments** are only allowed be putted in **faltten section**. Since share the args defined in section is sick www ~   

---

### Bug Fixed 🐛
#### Since the List and Section share the same symbol in config file, the refactor version of easy_config have some trobule with it. Now, the bug should be fixed, feel safe to use. 
---

### Simple Unittest 🧪
If you clone this repo and built from source, you can try to run the unittest.
`cd test && python test_Configer.py`

---

### License
MIT License. More information of each term, please see LICENSE.md

### Author 
Josef-Huang, a3285556aa@gmail.com 

### Footer
~ Hope God bless everyone in the world to know his word ~ <br>
**The fear of the LORD is the beginning of knowledge; fools despise wisdom and instruction. by Proverbs 1:7**