import os

from setuptools import setup, find_packages

with open('README.rst', encoding='utf-8') if os.path.exists('README.rst') else \
        open('README.md', encoding='utf-8') as fileobj:
    long_description = fileobj.read()

setup(
    name='mimo',
    version='1.0.10',
    author='Liam H. Childs',
    author_email='liam.h.childs@gmail.com',
    packages=find_packages(exclude=['tests']),
    url='https://github.com/childsish/mimo',
    license='LICENSE.txt',
    description='A streaming multi-input, multi-output Python library',
    long_description=long_description,
    install_requires=['lhc-python'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics']
)
