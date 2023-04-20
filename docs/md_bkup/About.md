#### easy_configer version : 1.3.4

### Configeruating the program in an easy-way ✨
This is a light-weight solution for configurating the python program. <br>
Hope this repository make every user control their large project with easier ~ ~ 

### Introduction 📝
With the large python project, a lot of argument will be required to control the business logic, user may need a simple way to load configurations through a file eventually. Their exists various package cover part of function with each other, and offer some solution to tackle the mentioned problem. 

**But at least I can not find a solution for load & use the argument in simple manner.**   Instead, most of them seems for the specific goal, and cause the code more longer and hard to read.

For example :
    
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
    

That's why I packaged my solution to this issue. The easy_config will have following attribute :

1. **simple & customized syntax of declaration (partially support)**

2. **Accept multiple config file with dynamic style**

3. **Declare customized class instance in the config file (partially support)**

4. **Commend-line update default value**

5. **Support the absl style FLAGS functionality** 

And, of course the following attribute will also be supported :

* dot-access of any default argument (flatten argument)

* dict-access of any section argument (non-flatten argument) 

* commend-line update any argument value (flatten & non-flatten argument)

* add different settings while choosing to overload previous one.

* inline comment '#', now you can write comment in everyline ~

* support arguments (flatten) interpolation!!

* support config conversion, which bridge the easy_config into the other config file ~