#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
>>> from prereform2modern import Processor
>>> text = "Онъ стоялъ подлѣ письменнаго стола"

>>> print Processor.process_text(
    text.decode('utf-8'),
    [u'@', u'{', u'}'],
    [u'', u'{', u'}'],
    1,
    print_log=False
    )[0]

Он{Онъ} стоял{стоялъ} подле{подлѣ} письменного{письменнаго} стола
"""

from unittest import TestCase

from prereform2modern import Processor


class TestProcess(BaseCase):
    
