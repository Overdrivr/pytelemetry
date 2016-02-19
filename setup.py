from setuptools import setup, find_packages, Extension
from codecs import open
from os import path
from setuptools.dist import Distribution
import pypandoc

try:
   description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError) as e:
    print("ERROR : Could not convert README.md. Fallback")
    print(e)
    description = open('README.md').read()

setup(
    name='pytelemetry',

    version='1.1.2',

    description='Lightweight remote monitoring and control of embedded devices',
    long_description=description, # Not working !

    url='https://github.com/Overdrivr/pytelemetry',

    author='Rémi Bèges',
    author_email='remi.beges@gmail.com',

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Telecommunications Industry',
        'Topic :: Communications',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: Software Development :: Libraries :: Python Modules',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
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
