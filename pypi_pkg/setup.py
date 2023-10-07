from setuptools import setup, find_packages
from os.path import abspath, join, dirname


# read the contents of your README file
this_directory = abspath(dirname(__file__))
with open(join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='easy_configer',
    version='2.1.2',
    description='An easy way for configurating python program by the given config file or config str',
    author='JosefHuang',
    author_email='a3285556aa@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/HuangChiEn/easy_config',
    packages=['easy_configer', 'easy_configer/utils', 'assets'],
    keywords=["configuration", "commendline argument", "argument"],
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
	    'Programming Language :: Python :: 3.9'
    ]
)