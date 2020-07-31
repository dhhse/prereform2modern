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
import json

from unittest import TestCase

from prereform2modern.process import Processor


class TestProcess(TestCase):
    def test_process_text_all_args_false(self):
        orig_text = u'Онъ стоялъ подлѣ письменнаго стола.'
        text_res, changes, w_edits, _json = Processor.process_text(
            orig_text, '', '', '', ''
            )

        t_expected = u'Он стоял подле письменного стола.'
        self.assertEqual(text_res, t_expected)

        changes_expected = u'Онъ --> Он\n\
стоялъ --> стоял\n\
подлѣ --> подле\n\
письменнаго --> письменного'
        self.assertEqual(changes, changes_expected)

        expected_wrong_edits = []
        self.assertListEqual(w_edits, expected_wrong_edits)

        _json = json.loads(_json)
        word_res = _json[u'6'][u'word']
        old_word_res = _json[u'6'][u'old_word']
        word_expected = u'письменного'
        old_word_expected = u'письменнаго'
        self.assertEqual(word_res, word_expected)
        self.assertEqual(old_word_res, old_word_expected)

    def test_process_text_with_delimiters(self):
        text = u'Онъ стоялъ подлѣ письменнаго стола.'
        text_res, changes, w_edits, _json = Processor.process_text(
            text=text,
            show=True,
            delimiters=[u'', u'{', u'}'],
            check_brackets=False,
            print_log=False
            )
        t_expected = u'Он{Онъ} стоял{стоялъ} подле{подлѣ} письменного{письменнаго} стола.'
        self.assertEqual(text_res, t_expected)

        # The rest is the same as in the previous test
        changes_expected = u'Онъ --> Он\n\
стоялъ --> стоял\n\
подлѣ --> подле\n\
письменнаго --> письменного'
        self.assertEqual(changes, changes_expected)

        expected_wrong_edits = []
        self.assertListEqual(w_edits, expected_wrong_edits)

        _json = json.loads(_json)
        word_res = _json[u'6'][u'word']
        old_word_res = _json[u'6'][u'old_word']
        word_expected = u'письменного'
        old_word_expected = u'письменнаго'
        self.assertEqual(word_res, word_expected)
        self.assertEqual(old_word_res, old_word_expected)
