# -*- coding: utf-8 -*-
__author__ = 'ElenaSidorova'
import re
# symbols = {u'і':u'i', u' {2,}':u' ', u'ъ':u'ъ', u"''":u'"'}
symbols = {u'і':u'i', u'ъ':u'ъ', u"''":u'"'}

class Preprocessor(object):
    @classmethod
    def preprocess_text(cls, text):
        for key in symbols.keys():
            text = re.sub(key, symbols[key], text)
        return text