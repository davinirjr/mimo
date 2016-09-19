import os

from setuptools import setup, find_packages

long_description = open('README.rst').read() if os.path.exists('README.rst') else\
    open('README.md').read()

setup(
    name='mimo',
    version='1.0.01',
    author='Liam H. Childs',
    author_email='liam.h.childs@gmail.com',
    packages=find_packages(exclude=['tests']),
    url='https://github.com/childsish/mimo',
    license='LICENSE.txt',
    description='A streaming multi-input, multi-output Python library',
    long_description=long_description,
    install_requires=['lhc-python']
)
