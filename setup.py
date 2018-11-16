#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from codecs import open
from os import path

DIR = path.abspath(path.dirname(__file__))

with open(path.join(DIR, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='tm-abci',
    version='0.6.3',
    description='Python based ABCI Server for Tendermint',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url='https://github.com/SoftblocksCo/tm-abci',
    author='SoftblocksCo',
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='blockchain tendermint abci',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        "protobuf>=3.6.1",
        "asyncio>=3.4.3",
        "colorlog>=3.1.2",
        "pytest>=3.5.0",
        "pytest-pythonpath>=0.7.2",
        "pytest-cov>=2.5.1"
    ],
    python_requires='>=3.6',
)
