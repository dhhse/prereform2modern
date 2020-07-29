#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This module contains tests for translit_from_string.

My setup for running this module is as follows:
# in directory prereform2modern/

$ python -m pip install --user virtualenv
$ virtualenv .venv --python=python2.7
$ source .venv/bin/activate
(.venv) $ ../.venv/bin/pip install pytest
(.venv) $ ../.venv/bin/python2.7 -m pytest

This test module can also be run as follows:
$ python2.7 -m unittest -v tests.system.test_process


>>> from prereform2modern import Processor
>>> text = "Онъ стоялъ подлѣ письменнаго стола"

>>> print Processor.process_text(
    text=text.decode('utf-8'),
    show=False,
    delimiters=[u'', u'{', u'}'],
    check_brackets=True,
    print_log=False
    )[0]

Он{Онъ} стоял{стоялъ} подле{подлѣ} письменного{письменнаго} стола
"""

from unittest import TestCase

from prereform2modern import Processor


class TestProcess(TestCase):
    def test_process_text_all_args_false(self):
        text = 'Онъ стоялъ подлѣ письменнаго стола.'
        try:  # support for Py2
            result = Processor.process_text(
                text.decode('utf-8'), '', '', '', ''
                )[0]
        except AttributeError:  # support for Py3
            result = Processor.process_text(
                text, '', '', '', ''
                )[0]
        expected = u'Он стоял подле письменного стола.'
        self.assertEqual(result, expected)

    def test_process_text_with_delimiters(self):
        text = 'Онъ стоялъ подлѣ письменнаго стола.'
        try:  # support for Py2
            result = Processor.process_text(
                text=text.decode('utf-8'),
                show=False,
                delimiters=[u'', u'{', u'}'],
                check_brackets=True,
                print_log=False
                )[0]
        except AttributeError:  # support for Py3
            result = Processor.process_text(
                text,
                text=text.decode('utf-8'),
                show=False,
                delimiters=[u'', u'{', u'}'],
                check_brackets=True,
                print_log=False
                )[0]
        expected = u'Он{Онъ} стоял{стоялъ} подле{подлѣ} письменного{письменнаго} стола.'
        self.assertEqual(result, expected)
