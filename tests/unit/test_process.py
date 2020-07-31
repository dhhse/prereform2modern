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

(.venv) $ ../.venv/bin/python2.7 -m pytest tests/unit/test_process.py


#########################################################################
This test can be run in Py3:
$ python3 -m pytest tests/unit/test_process.py
Provided that the module transliterator.py is blank except for the following
lines:
    class Transliterator:
        def transliterate(self):
            pass
Otherwise, this module causes SyntaxError in line 13:
E       re.compile(ur'^воз([пткфсцчщшх].*)', flags=34):ur'вос\1',
E                                         ^
#########################################################################


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
                self.plain_word = None
                self.old_plain_word = None

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

        orig_text = u'Онъ'
        text_res, changes, w_edits, _json = Processor.process_text(
            orig_text, '', '', '', ''
            )

        t_expected = u'Он'
        self.assertEqual(text_res, t_expected)

        changes_expected = u'Онъ --> Он'
        self.assertEqual(changes, changes_expected)

        expected_wrong_edits = []
        self.assertListEqual(w_edits, expected_wrong_edits)

        _json = json.loads(_json)
        word_res = _json[u'0'][u'word']
        old_word_res = _json[u'0'][u'old_word']
        word_expected = u'Он'
        old_word_expected = u'Онъ'
        self.assertEqual(word_res, word_expected)
        self.assertEqual(old_word_res, old_word_expected)
