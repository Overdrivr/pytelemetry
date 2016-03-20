# -*- coding: utf-8 -*-

from setuptools import setup, find_packages, Extension
from codecs import open
from os import path
from setuptools.dist import Distribution
import io

with io.open('DESCRIPTION.rst', encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='pytelemetry',

    version='1.1.9',

    description='First class data visualization and communication with embedded devices',
    long_description=long_description,

    url='https://github.com/Overdrivr/pytelemetry',

    author='Rémi Bèges',
    author_email='remi.beges@gmail.com',

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Intended Audience :: Telecommunications Industry',
        'Topic :: Communications',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='lightweight communication protocol embedded telemetry remote program control',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['tests']),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['pyserial','enum34'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': ['check-manifest'],
        'test': ['pytest','pytest-cov'],
    },
)
