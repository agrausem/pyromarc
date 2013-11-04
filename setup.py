#!/usr/bin/env python

from setuptools import setup
from setuptools import find_packages

with open('README.rst') as readme:
    long_description = readme.read()

with open('requirements.txt') as requirements:
    lines = requirements.readlines()
    libraries = [lib for lib in lines if not lib.startswith('-')]

setup(
    name='pyromarc',
    version='0.1',
    author='Arnaud Grausem',
    author_email='arnaud.grausem@gmail.com',
    maintainer='Arnaud Grausem',
    maintainer_email='arnaud.grausem@gmail.com',
    url='https://github.com/agrausem/pyromarc',
    license='PSF',
    description='Python implementation of MARC:MIR',
    long_description=long_description,
    packages=find_packages(),
    download_url='http://pypi.python.org/pypi/pyromarc',
    install_requires=libraries,
    keywords=[],
    entry_points={},
    classifiers = (
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    )
)
