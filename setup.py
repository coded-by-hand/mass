#!/usr/bin/env python

#pandoc -t rst -f markdown README.mkd -o README

import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='mass',
    version='0.1.4',
    description='Merge and Simplify Scripts: an automated tool for managing, combining and minifying javascript assets for web projects.',
    long_description=read('README'),
    author='jack boberg alex padgett',
    author_email='info@codedbyhand.com',
    url='https://github.com/coded-by-hand/mass',
    license='BSD License',
    platforms=['Mac OSX'],
    packages=['mass'],
    install_requires=['distribute','jsmin','macfsevents'],
    zip_safe = False,
    entry_points = {
        'console_scripts': [
            "mass = mass.monitor:main"
        ],
    }
)
