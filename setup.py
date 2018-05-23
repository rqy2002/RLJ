#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from setuptools import setup, find_packages
import rlj

setup(
    name='rlj',
    version=rlj.__version__,
    description=rlj.__doc__.strip(),
    long_description=open('README.rst').read(),
    url='https://github.com/rqy1458814497/RLJ/',
    author=rlj.__author__,
    author_email='1458814497@qq.com',
    license=rlj.__license__,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'rlj = rlj.main:main',
        ],
    },
    install_requires=[
        'docopt>=0.6.2',
        'colorama>=0.3.9',
        'psutil>=5.4.1',
        'pyyaml>=3.12',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Information Technology',
    ],
)
