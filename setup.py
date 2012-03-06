#!/usr/bin/env python

from setuptools import setup

setup(
    name='mass',
    version='0.0.1',
    description='Watches your javascript',
    author='Jack Boberg & Alex Padgett',
    author_email='developer@topicdesign.com',
    url='https://github.com/jackboberg/jswatchr',
    packages=['mass'],
    install_requires=['distribute','jsmin','macfsevents'],
    zip_safe = False,
    entry_points = {
        'console_scripts': [
            "mass = mass.monitor:main"
        ],
    }
)
