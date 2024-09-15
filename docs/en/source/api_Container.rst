.. role:: raw-html-m2r(raw)
   :format: html


utils.Container
=================


* `utils.Container <#utils.Container>`_

  * `AttributeDict <#utils.Container.AttributeDict>`_

    * `__init__ <#utils.Container.AttributeDict.\_\_init\_\_>`_
    * `__getattribute__ <#utils.Container.AttributeDict.\_\_getattribute\_\_>`_
    * `__getattr__ <#utils.Container.AttributeDict.\_\_getattr\_\_>`_
    * `set_attr_dict <#utils.Container.AttributeDict.set_attr_dict>`_
    * `__setattr__ <#utils.Container.AttributeDict.\_\_setattr\_\_>`_
    * `__setitem__ <#utils.Container.AttributeDict.\_\_setitem\_\_>`_
    * `__deepcopy__ <#utils.Container.AttributeDict.\_\_deepcopy\_\_>`_
    * `__getstate__ <#utils.Container.AttributeDict.\_\_getstate\_\_>`_
    * `__setstate__ <#utils.Container.AttributeDict.\_\_setstate\_\_>`_

  * `Flag <#utils.Container.Flag>`_

    * `__new__ <#utils.Container.Flag.\_\_new\_\_>`_
    * `FLAGS <#utils.Container.Flag.FLAGS>`_


:raw-html-m2r:`<a id="utils.Container.AttributeDict"></a>`

AttributeDict
--------------

.. code-block:: python

   class AttributeDict(dict)

A dict-like container to store nested arguments defined in config.
Since the container inherit python native dict (base class), we simply store 
arguments in the base dict with such navie way : ``dict[key] = value``\ ,
by calling super().\ **setitem**\ (key, value) in subclass. self.\ **setattr** 
also call super().\ **setitem** underhood! According to the way we store args, 
we access args by the navie way self[key] (namely, dict[key]). 
Additionally, we build the getattr guard for implement the defaultdict functionality.
self.\ **getitem** no need to override, just as same as base class.

:raw-html-m2r:`<a id="utils.Container.AttributeDict.__init__"></a>`

__init__
~~~~~~~~

.. code-block:: python

   def __init__(init_dict={})

Constructor of container.

**Arguments**\ :


* ``init_dict`` *dict* - typically it'll be value dict parsed in Configer. Default to empty dict.

**Returns**\ :

  None.

:raw-html-m2r:`<a id="utils.Container.AttributeDict.__getattribute__"></a>`

__getattribute__
~~~~~~~~~~~~~~~~

.. code-block:: python

   def __getattribute__(attr)

Override **getattribute** dunder method. Since we apply base class (dict) 
to store all args, self.\ **dict** should not be used in anyway.

Raise:
    Runtime Error, while user attempt to access self.\ **dict**.

:raw-html-m2r:`<a id="utils.Container.AttributeDict.__getattr__"></a>`

__getattr__
~~~~~~~~~~~

.. code-block:: python

   def __getattr__(key)

Override **getattr** dunder method to silently build the 'empty dict'.
So that we can assign value to the specific argument without define their parent dict.
Note : same behavior as defaultdict, allow recursively self.\ **setattr**.

**Returns**\ :

  AttributeDict, the returned dict have pre-defined empty dict,
  then the specific argument could be updated to the empty dict.

:raw-html-m2r:`<a id="utils.Container.AttributeDict.set_attr_dict"></a>`

set_attr_dict
~~~~~~~~~~~~~

.. code-block:: python

   def set_attr_dict(raw_dict)

Make input dict become AttributeDict instance, call **setitem** underhood.

**Arguments**\ :


* ``raw_dict`` *dict* - python native dict, it'll be turn into AttributeDict after calling this method.

:raw-html-m2r:`<a id="utils.Container.AttributeDict.__setattr__"></a>`

__setattr__
~~~~~~~~~~~

.. code-block:: python

   def __setattr__(key, value)

Override **setattr** dunder method. call **setitem** underhood.

:raw-html-m2r:`<a id="utils.Container.AttributeDict.__setitem__"></a>`

__setitem__
~~~~~~~~~~~

.. code-block:: python

   def __setitem__(key, value)

Override **setitem** dunder method. Wrap any input value with AttributeDict container.

:raw-html-m2r:`<a id="utils.Container.AttributeDict.__deepcopy__"></a>`

__deepcopy__
~~~~~~~~~~~~

.. code-block:: python

   def __deepcopy__(memo=None)

Support deepcopy, src:https://stackoverflow.com/questions/49901590/python-using-copy-deepcopy-on-dotdict.

:raw-html-m2r:`<a id="utils.Container.AttributeDict.__getstate__"></a>`

__getstate__
~~~~~~~~~~~~

.. code-block:: python

   def __getstate__()

Basic serialized interface (i.e. pickle). Return serielized python object.

:raw-html-m2r:`<a id="utils.Container.AttributeDict.__setstate__"></a>`

__setstate__
~~~~~~~~~~~~

.. code-block:: python

   def __setstate__(de_ser_self)

Basic serialized interface (i.e. pickle). Accept de-serielized object, replace default self into it.

:raw-html-m2r:`<a id="utils.Container.Flag"></a>`

Flag
----

.. code-block:: python

   class Flag(object)

A synchronized object to defined config in Configer. It's inspired by absl flag in tensorflow. 
Although this is not useful, but we keep this class for competible with easy_config early version.
You still can use it.

:raw-html-m2r:`<a id="utils.Container.Flag.__new__"></a>`

__new__
~~~~~~~

.. code-block:: python

   def __new__(cls, *args, **kwargs)

Override **new** dunder method. **new** is used to create the class before calling **init**\ ,
so we set the singleton guard in here for implement the singleton design pattern.

**Arguments**\ :

  `*args, **kwargs` : will be passed into FLAG_spec instance, which is the singleton instance.

**Returns**\ :

  FLAG_spec, a sync object of config.

:raw-html-m2r:`<a id="utils.Container.Flag.FLAGS"></a>`

FLAGS
~~~~~

.. code-block:: python

   @property
   def FLAGS()

Interface to access FLAG_spec object.
