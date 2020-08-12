#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This module contains some unit tests for translit_from_string.

This test can be run in Py3:
$ python3 -m pytest tests/unit/test_process.py

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

try:
    from unittest.mock import patch  # Python 3
except ImportError:
    from mock import patch  # Python 2.7, to be run with pytest


def context_decorator(func):
    def return_function(self):
        class FakeTokens:
            """Help create a fake response from Tokenizer.tokenize()."""
            def __init__(self):
                self.type = u'word'
                self.word = u'Онъ'
                self.old_word = u''
                # self.plain_word = None
                # self.old_plain_word = None

        fake_tokens = FakeTokens()
        tok_returns = {0: fake_tokens}

        with patch(
          'prereform2modern.preprocess.Preprocessor.preprocess_text',
          return_value=u'Онъ'):
            with patch(
              'prereform2modern.tokenizer.Tokenizer.tokenize',
              return_value=tok_returns):
                with patch(
                  'prereform2modern.transliterator.Transliterator.transliterate',
                  return_value=u'Он'):
                    func(self)
    return return_function


class TestProcess(TestCase):

    @context_decorator
    def test_process_text_all_args_false(self):
        """process_text should return 4 expected values."""
        orig_text = u'Онъ'
        # Call with all patams False except the 'text' parameter
        text_res, changes, _json = Processor.process_text(
            orig_text, '', '', ''
            )

        t_expected = u'Он'
        self.assertEqual(text_res, t_expected)

        changes_expected = u'Онъ --> Он'
        self.assertEqual(changes, changes_expected)

        json_obj = json.loads(_json)
        expected_json = {
            u'0': {u'word': u'Он',
                   # u'plain_word': None,
                   u'type': u'word',
                   u'old_word': u'Онъ',
                   # u'old_plain_word': None
                   }
        }
        self.assertDictEqual(json_obj, expected_json)

    @context_decorator
    def test_process_text_with_delimiters(self):
        orig_text = u'Онъ'
        text_res, changes, _json = Processor.process_text(
            text=orig_text,
            show=True,
            delimiters=[u'', u'{', u'}'],
            check_brackets=False,
            # print_log=False
            )
        t_expected = u'Он{Онъ}'
        self.assertEqual(text_res, t_expected)

        changes_expected = u'Онъ --> Он'
        self.assertEqual(changes, changes_expected)

        json_obj = json.loads(_json)
        expected_json = {
            u'0': {u'word': u'Он',
                   # u'plain_word': None,
                   u'type': u'word',
                   u'old_word': u'Онъ',
                   # u'old_plain_word': None
                   }
        }
        self.assertDictEqual(json_obj, expected_json)

    def test_process_text_old_style_correction_in_brackets_check_false(self):
        class FakeTokens:
            """Help create a fake response from Tokenizer.tokenize()."""
            def __init__(self):
                self.type = u'word'
                self.word = u'обычно[мъ]'
                self.old_word = u''
                # self.plain_word = None
                # self.old_plain_word = None

        fake_tokens = FakeTokens()
        tok_returns = {0: fake_tokens}

        with patch(
          'prereform2modern.preprocess.Preprocessor.preprocess_text',
          return_value=u'обычно[мъ]'):
            with patch(
              'prereform2modern.tokenizer.Tokenizer.tokenize',
              return_value=tok_returns):
                with patch(
                  'prereform2modern.transliterator.Transliterator.transliterate',
                  return_value=u'обычно[м]'):

                    orig_text = u'обычно[мъ]'
                    text_res, changes, _json = Processor.process_text(
                        text=orig_text,
                        show=False,
                        delimiters=[u'', u'{', u'}'],
                        check_brackets=False,  # This is different
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
