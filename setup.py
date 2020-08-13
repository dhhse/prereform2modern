#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os

import setuptools

from prereform2modern import __version__


# Package meta-data.
NAME = 'prereform2modern'
DESCRIPTION = 'Pre-reform to contemporary orthography convertor for the Russian language'
URL = 'https://github.com/dhhse/prereform2modern'
EMAIL = 'dskorinkin@hse.ru'
AUTHOR = 'Elena Sidorova'
REQUIRES_PYTHON = '>=3.6.0,<4.0.0'

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
try:
    with io.open(os.path.join(here, 'readme.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION


setuptools.setup(
    name=NAME,
    version=__version__,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=setuptools.find_packages(exclude=('tests',)),
    # install_requires=list_reqs(),
    package_data={
        NAME: ['datasets/*.csv']
    },
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        # 'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='prereform contemporary orthography convertor Russian',
    entry_points={
        'console_scripts': [
            'translit=prereform2modern.translit_from_string:main',
        ],
    },
)
