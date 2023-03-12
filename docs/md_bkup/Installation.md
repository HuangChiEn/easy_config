
### Installation ⚙️<br>
1. **pypi install** <br>
    simply type the `pip install easy_configer` (due to name conflict of pypi pkg, we use different pkg name)
2. **install from source code** <br>
    clone the project from github : `git clone repo-link` 
    Chage to the root directory of the cloned project, and type `pip install -e .`
3. **import syntax** <br>
    Because of the name conflict of pypi pkg, i choice the different pkg name.
    To import the installed pkg, the syntax will be depended on the install method. For example. <br>
    Pip install : `from easy_configer.Configer import Configer` <br>
    git clone & pip install : `from easy_config.Configer import Configer` <br>
    
---

### Dependencies
This package is written for Python 3.8 (but 3.6+ may be supported).
Of course, light-weight solution **do not** contain any 3-rd package complex dependencies.
The python standard package (such as pathlib, sys, .., etc) is the only source of dependencies, so you don't need to worry about that ~ ~
> However, if you want to use the IO_Converter (config conversion mechnaism), you still need to install omegaconf for integrate with hydra ~

---