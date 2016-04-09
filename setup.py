#!/usr/bin/env python

from distutils.core import setup

setup(
    name='PyCraft',
    version='0.1',
    description='PyCraft',
    packages=['pycraft'],
    install_requires=[
        'pyglet',
        'noise',
    ],
)
