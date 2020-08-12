#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This module contains tests for word_tokenize.

You can run this with:
python2.7 -m unittest -v tests.unit.test_word_tokenize
or
python3 -m unittest -v tests.unit.test_word_tokenize

"""

from unittest import TestCase

from prereform2modern.word_tokenize import WordTokenizer


class TestWordTokenizer(TestCase):

    def test_tokenize_alphabetical_text(self):
        # Этот тест работает и в Py2, и в Py3
        text = u"Онъ стоялъ подлѣ письменнаго стола."
        result = WordTokenizer.tokenize(text)
        expected = [u'Онъ',
                    u' ',
                    u'стоялъ',
                    u' ',
                    u'подлѣ',
                    u' ',
                    u'письменнаго',
                    u' ',
                    u'стола',
                    u'.'
                    ]
        self.assertListEqual(result, expected)

        # TODO: Если в метод tokenize() подать u'[', то он работает
        # в Py2, но не работает в Py3 из-за ошибки "NameError: name 'unicode'
        # is not defined", поэтому хорошо бы для этого случая написать тест
        #
        # Хорошо бы также посмотреть, предполагается ли вызывать этот метод
        # с чем-либо, кроме чистого текста, может какие-то теги и т.п.
        #
        # В общем, попытаться найти какие-то случаи, в которых код работает в
        # Py2, но возможно не стал бы работать также в Py3

    # def test_tokenize_opening_bracket(self):
    #     # TODO:
    #     pass
