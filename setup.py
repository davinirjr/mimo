import os

from setuptools import setup, find_packages

long_description = open('README.rst').read() if os.path.exists('README.rst') else\
    open('README.md').read()

setup(
    name='mimo',
    version='1.0.0',
    author='Liam H. Childs',
    author_email='liam.h.childs@gmail.com',
    packages=find_packages(exclude=['test']),
    url='https://github.com/childsish/mimo',
    license='LICENSE.txt',
    description='A Python multi-input, multi-output streaming library',
    long_description=long_description,
    install_requires=['lhc-python']
)
