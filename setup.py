#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup.py file for Hydraulics.
"""
from __future__ import unicode_literals

import os
import re
from setuptools import setup, find_packages


cwd = os.path.abspath(os.path.dirname(__file__))

# ----------------------------------------------------------------------
#  Package internal data
# ----------------------------------------------------------------------
project_name = 'pycraft'

classifiers = [
    'Programming Language :: Python',
    'Natural Language :: English',
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: MIT',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.5',
]

# Populates package metadata from project internals
package_name = project_name
pattern = r"^__(?P<key>(.*?))__ = '(?P<value>([^']*))'"
engine = re.compile(pattern)
with open(os.path.join(cwd, project_name, '__init__.py'), 'r') as fd:
    metadata = {
        data['key']: data['value']
        for line in fd
        for data in [m.groupdict() for m in engine.finditer(line)]
    }

# ----------------------------------------------------------------------
#  Top level package requirements defined
# ----------------------------------------------------------------------

# Package requirements for execution
requirements = [
    'future',
    'pyglet',
    'noise',
]

# Testing requirements
tests_requirements = [
    'mock',
    'pyyaml',
    'pytest',
    'pytest-flake8',
    'pytest-cov',
    'pytest-xdist'
]

# Documentation requirements
doc_requirements = [
    'sphinx',
    'sphinx_rtd_theme',
]

# Intended for developers
developer_requirements = [
    'ipython',
    'bpython',
    'ipdb',
]

# Include all available requirements
all_requirements = []
all_requirements.extend(requirements)
all_requirements.extend(tests_requirements)
all_requirements.extend(doc_requirements)
all_requirements.extend(developer_requirements)

# packages = find_packages(include=(namespace,))
packages = find_packages()

lic = open(os.path.join(cwd, 'LICENSE'), 'rb').read()
lic = lic.decode('utf-8')

# ----------------------------------------------------------------------
#  Create package
# ----------------------------------------------------------------------
setup(
    # Package information
    name=package_name,
    version=metadata.get('versionstr', '0.1.0'),
    description=metadata.get('shortdoc', package_name),
    long_description=metadata.get('doc', ''),
    url=metadata.get('url', ''),
    license=lic,
    author=metadata.get('author'),
    author_email=metadata.get('email'),

    # Package Properties
    packages=packages,
    include_package_data=True,
    platforms=['any'],
    classifiers=classifiers,
    zip_safe=False,

    # Requirements
    setup_requires=['pip'],
    install_requires=requirements,
    extras_require={
        'all': all_requirements,
        'tests': tests_requirements,
        'dev': developer_requirements,
        'docs': doc_requirements,
    },
    tests_require=tests_requirements,

    # Scripts and execution
    entry_points={
        'console_scripts': [
            'pycraft=pycraft.main:main'
        ]
    },
)
