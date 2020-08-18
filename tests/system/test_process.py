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
OR $ ../.venv/bin/python2.7 -m pytest -v tests/system/test_process.py

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
        text_res, changes, _json = Processor.process_text(
            orig_text, '', '', ''
            )

        t_expected = u'Он стоял подле письменного стола.'
        self.assertEqual(text_res, t_expected)

        changes_expected = u'Онъ --> Он\n\
стоялъ --> стоял\n\
подлѣ --> подле\n\
письменнаго --> письменного'
        self.assertEqual(changes, changes_expected)

        _json = json.loads(_json)
        word_res = _json[u'6'][u'word']
        old_word_res = _json[u'6'][u'old_word']
        word_expected = u'письменного'
        old_word_expected = u'письменнаго'
        self.assertEqual(word_res, word_expected)
        self.assertEqual(old_word_res, old_word_expected)

    def test_process_text_with_delimiters(self):
        text = u'Онъ стоялъ подлѣ письменнаго стола.'
        text_res, changes, _json = Processor.process_text(
            text=text,
            show=True,
            delimiters=[u'', u'{', u'}'],
            check_brackets=False,
            # print_log=False
            )
        t_expected = u'Он{Онъ} стоял{стоялъ} подле{подлѣ} письменного{письменнаго} стола.'
        self.assertEqual(text_res, t_expected)

        # The rest is the same as in the previous test
        changes_expected = u'Онъ --> Он\n\
стоялъ --> стоял\n\
подлѣ --> подле\n\
письменнаго --> письменного'
        self.assertEqual(changes, changes_expected)

        _json = json.loads(_json)
        word_res = _json[u'6'][u'word']
        old_word_res = _json[u'6'][u'old_word']
        word_expected = u'письменного'
        old_word_expected = u'письменнаго'
        self.assertEqual(word_res, word_expected)
        self.assertEqual(old_word_res, old_word_expected)

    def test_process_text_with_editorial_correction_in_brackets(self):
        orig_text = u'такъ [называемую]'
        text_res, changes, _json = Processor.process_text(
            text=orig_text,
            show=False,
            delimiters=[u'', u'{', u'}'],
            check_brackets=True,
            # print_log=False
            )

        t_expected = u"так{такъ} <choice original_editorial_correction='[называемую]'><sic></sic><corr>называемую</corr></choice>"
        self.assertEqual(text_res, t_expected)

        changes_expected = u'такъ	-->	так'
        self.assertEqual(changes, changes_expected)

        json_obj = json.loads(_json)
        expected_json = {
            u'1': {u'word': u' ',
                   # u'plain_word': None,
                   u'type': u'punct',
                   u'old_word': u'',
                   # u'old_plain_word': None
                   },
            u'0': {u'word': u'так',
                   # u'plain_word': None,
                   u'type': u'word',
                   u'old_word': u'такъ',
                   # u'old_plain_word': None
                   },
            u'2': {u'word': u'[называемую]',
                   # u'plain_word': None,
                   u'type': u'word',
                   u'old_word': u'',
                   # u'old_plain_word': None
                   }
        }
        self.assertDictEqual(json_obj, expected_json)

    def test_process_text_with_edit_corr_in_brackets_false_brackets(self):
        orig_text = u'такъ [называемую]'
        text_res, changes, _json = Processor.process_text(
            text=orig_text,
            show=False,
            delimiters=[u'', u'{', u'}'],
            check_brackets=False,  # This is different from the test above
            # print_log=False
            )

        t_expected = u'так [называемую]'
        self.assertEqual(text_res, t_expected)

        changes_expected = u'такъ --> так'
        self.assertEqual(changes, changes_expected)

        json_obj = json.loads(_json)
        expected_json = {
            u'1': {u'word': u' ',
                   # u'plain_word': None,
                   u'type': u'punct',
                   u'old_word': u'',
                   # u'old_plain_word': None
                   },
            u'0': {u'word': u'так',
                   # u'plain_word': None,
                   u'type': u'word',
                   u'old_word': u'такъ',
                   # u'old_plain_word': None
                   },
            u'2': {u'word': u'[называемую]',
                   # u'plain_word': None,
                   u'type': u'word',
                   u'old_word': u'',
                   # u'old_plain_word': None
                   }
        }
        self.assertDictEqual(json_obj, expected_json)

    def test_process_text_with_digits_in_brackets(self):
        orig_text = u'такъ [13]'
        text_res, changes, _json = Processor.process_text(
            text=orig_text,
            show=False,
            delimiters=[u'', u'{', u'}'],
            check_brackets=True,
            # print_log=False
            )

        t_expected = u"так{такъ} [13]"
        self.assertEqual(text_res, t_expected)

        changes_expected = u'такъ	-->	так'
        self.assertEqual(changes, changes_expected)

        json_obj = json.loads(_json)
        expected_json = {
            u'1': {u'word': u' ',
                   # u'plain_word': None,
                   u'type': u'punct',
                   u'old_word': u'',
                   # u'old_plain_word': None
                   },
            u'0': {u'word': u'так',
                   # u'plain_word': None,
                   u'type': u'word',
                   u'old_word': u'такъ',
                   # u'old_plain_word': None
                   },
            u'3': {u'word': u'13',
                   # u'plain_word': None,
                   u'type': u'punct',
                   u'old_word': u'',
                   # u'old_plain_word': None
                   },
            u'2': {u'word': u'[',
                   # u'plain_word': None,
                   u'type': u'punct',
                   u'old_word': u'',
                   # u'old_plain_word': None
                   },
            u'4': {u'word': u']',
                   # u'plain_word': None,
                   u'type': u'punct',
                   u'old_word': u'',
                   # u'old_plain_word': None
                   }
        }
        self.assertDictEqual(json_obj, expected_json)

    def test_process_text_with_empty_brackets_check_true(self):
        orig_text = u'такъ []'
        text_res, changes, _json = Processor.process_text(
            text=orig_text,
            show=False,
            delimiters=[u'', u'{', u'}'],
            check_brackets=True,
            # print_log=False
            )

        t_expected = u"так{такъ} []"
        self.assertEqual(text_res, t_expected)

        changes_expected = u'такъ	-->	так'
        self.assertEqual(changes, changes_expected)

        json_obj = json.loads(_json)
        expected_json = {
            u'1': {u'word': u' ',
                   # u'plain_word': None,
                   u'type': u'punct',
                   u'old_word': u'',
                   # u'old_plain_word': None
                   },
            u'0': {u'word': u'так',
                   # u'plain_word': None,
                   u'type': u'word',
                   u'old_word': u'такъ',
                   # u'old_plain_word': None
                   },
            u'3': {u'word': u']',
                   # u'plain_word': None,
                   u'type': u'punct',
                   u'old_word': u'',
                   # u'old_plain_word': None
                   },
            u'2': {u'word': u'[',
                   # u'plain_word': None,
                   u'type': u'punct',
                   u'old_word': u'',
                   # u'old_plain_word': None
                   }
        }
        self.assertDictEqual(json_obj, expected_json)

    def test_process_text_with_empty_brackets_check_false(self):
        orig_text = u'такъ []'
        text_res, changes, _json = Processor.process_text(
            text=orig_text,
            show=False,
            delimiters=[u'', u'{', u'}'],
            check_brackets=False,  # This is different from the test above
            # print_log=False
            )

        t_expected = u"так []"
        self.assertEqual(text_res, t_expected)

        changes_expected = u'такъ --> так'
        self.assertEqual(changes, changes_expected)

        json_obj = json.loads(_json)
        expected_json = {
            u'1': {u'word': u' ',
                   # u'plain_word': None,
                   u'type': u'punct',
                   u'old_word': u'',
                   # u'old_plain_word': None
                   },
            u'0': {u'word': u'так',
                   # u'plain_word': None,
                   u'type': u'word',
                   u'old_word': u'такъ',
                   # u'old_plain_word': None
                   },
            u'3': {u'word': u']',
                   # u'plain_word': None,
                   u'type': u'punct',
                   u'old_word': u'',
                   # u'old_plain_word': None
                   },
            u'2': {u'word': u'[',
                   # u'plain_word': None,
                   u'type': u'punct',
                   u'old_word': u'',
                   # u'old_plain_word': None
                   }
        }
        self.assertDictEqual(json_obj, expected_json)

    def test_process_text_empty_input(self):
        orig_text = u''
        text_res, changes, _json = Processor.process_text(
            text=orig_text,
            show=False,
            delimiters=[u'', u'{', u'}'],
            check_brackets=False,
            # print_log=False
            )

        t_expected = u''
        self.assertEqual(text_res, t_expected)

        changes_expected = u''
        self.assertEqual(changes, changes_expected)

        json_obj = json.loads(_json)
        expected_json = {}
        self.assertDictEqual(json_obj, expected_json)

    def test_process_text_old_style_correction_in_brackets_check_true(self):
        orig_text = u'обычно[мъ]'
        text_res, changes, _json = Processor.process_text(
            text=orig_text,
            show=False,
            delimiters=[u'', u'{', u'}'],
            check_brackets=True,
            # print_log=False
            )

        t_expected = u"<choice original_editorial_correction='обычно[мъ]'><sic>обычно</sic><corr>обычном{обычномъ}</corr></choice>"
        self.assertEqual(text_res, t_expected)

        changes_expected = u'обычно[мъ] --> обычно[м]'
        self.assertEqual(changes, changes_expected)

        json_obj = json.loads(_json)
        expected_json = {
            u'0': {u'word': u'обычно[м]',
                   # u'plain_word': None,
                   u'type': u'word',
                   u'old_word': u'обычно[мъ]',
                   # u'old_plain_word': None
                   }
        }
        self.assertDictEqual(json_obj, expected_json)

    def test_process_text_old_style_correction_in_brackets_check_false(self):
        orig_text = u'обычно[мъ]'
        text_res, changes, _json = Processor.process_text(
            text=orig_text,
            show=False,
            delimiters=[u'', u'{', u'}'],
            check_brackets=False,  # This is different from the test above
            # print_log=False
            )

        t_expected = u'обычно[м]'
        self.assertEqual(text_res, t_expected)

        changes_expected = u'обычно[мъ] --> обычно[м]'
        self.assertEqual(changes, changes_expected)

        json_obj = json.loads(_json)
        expected_json = {
            u'0': {u'word': u'обычно[м]',
                   # u'plain_word': None,
                   u'type': u'word',
                   u'old_word': u'обычно[мъ]',
                   # u'old_plain_word': None
                   }
        }
        self.assertDictEqual(json_obj, expected_json)
