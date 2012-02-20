#!/usr/bin/env python

from setuptools import setup

setup(
    name='jswatchr',
    version='0.0.1',
    description='Watches your javascript',
    author='Jack Boberg & Alex Padgett',
    author_email='developer@topicdesign.com',
    url='https://github.com/jackboberg/jswatchr',
    packages=['jswatchr'],
    install_requires=['distribute','jsmin','macfsevents'],
    zip_safe = False,
    entry_points = {
        'console_scripts': [
            "jswatchr = jswatchr.monitor:main"
        ],
    }
)
