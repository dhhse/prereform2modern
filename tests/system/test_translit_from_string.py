#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This module contains tests for translit_from_string.

My setup for running this module is as follows:
# in directory prereform2modern/

$ python -m pip install --user virtualenv
$ virtualenv .venv --python=python2.7
$ source .venv/bin/activate
(.venv) $ ../.venv/bin/pip install pytest
(.venv) $ ../.venv/bin/python2.7 -m pytest
"""

import sys

from unittest import TestCase

from prereform2modern.translit_from_string import main

if sys.version_info >= (3, 3):
    from io import StringIO  # Python 3
else:
    from StringIO import StringIO  # Python 2.7

try:
    from unittest.mock import patch  # Python 3
except ImportError:
    from mock import patch  # Python 2.7, to be run with pytest


class TestMain(TestCase):

    def test_main_prints_text(self):
        with patch(
            'sys.stdout',
            new_callable=StringIO
            ) as mock_stdout:
            main(
                ['',  # first arg to main is the script name
                 u'Онъ стоялъ подлѣ письменнаго стола'
                 ]
                )
            expected = u'Он стоял подле письменного стола'
            self.assertIn(
                expected,
                mock_stdout.getvalue().strip()
                )

    def test_main_prints_json(self):
        with patch(
            'sys.stdout',
            new_callable=StringIO
        ) as mock_stdout:
            main(
                ['',
                 '-t',
                 u'Онъ стоялъ подлѣ письменнаго стола'
                 ]
                )
            expected = u'Он{Онъ} стоял{стоялъ} подле{подлѣ} письменного{письменнаго} стола'
            self.assertIn(
                expected,
                mock_stdout.getvalue().strip()
                )
