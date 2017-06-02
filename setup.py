#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# package setup
# 
# @author <bprinty@gmail.com>
# ------------------------------------------------


# config
# ------
import os
import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open(os.path.join('gems', '__init__.py'), 'r') as fi:
    __version__ = re.search(r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fi.read()).group(1)


with open('requirements.txt', 'r') as reqs:
    requirements = map(lambda x: x.rstrip(), reqs.readlines())


test_requirements = [
    'nose',
    'nose-parameterized'
]


# files
# -----
with open('README.rst') as readme_file:
    readme = readme_file.read()


# exec
# ----
setup(
    name='gems',
    version=__version__,
    description="Python utilities for data manipulation and management.",
    long_description=readme,
    author="Blake Printy",
    author_email='bprinty@gmail.com',
    url='https://github.com/bprinty/gems',
    packages=['gems'],
    package_dir={'gems': 'gems'},
    include_package_data=True,
    install_requires=requirements,
    license="Apache-2.0",
    zip_safe=False,
    keywords=['gems', 'data', 'structures', 'types', 'filesystem', 'management'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apple Public Source License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='nose.collector',
    tests_require=test_requirements
)
