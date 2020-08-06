# -*- coding: utf-8 -*-
__author__ = 'ElenaSidorova'
import codecs
import os

PACKAGE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = 'datasets'

dicts = [
    'freq.csv',
    'ozhegov.csv',
    'sharov.csv',
    'ushakov.csv',
    'zaliznyak.csv'
]
wrong_dicts = [
    'adjectives_ija_ends.csv',
    'perfect_verbs.csv'
]
ok_dicts = [
    'soft_sign_ends.csv'
]
prefixes = [
    'all_prefixes.csv'
]
class DictLoader(object):
    @classmethod
    def load_dicts(cls):
        named_dicts = cls.read_data(dicts)
        wrong = cls.read_data(wrong_dicts)
        ok = cls.read_data(ok_dicts)
        all_prefixes = cls.read_data(prefixes)
        dict_settings = [named_dicts, wrong, ok, all_prefixes]
        return dict_settings

    @classmethod
    def read_data(cls, arr):
        result = []
        for d in arr:
            with codecs.open(os.path.join(PACKAGE_DIR, DATA_DIR, d), 'r', 'utf-8') as inf:
                data = inf.read().strip()
            data = data.replace(u'\r', u'').lower().split(u'\n')
            if 'freq' in d:
                new = []
                for el in data:
                    new.append(el.split()[0])
                data = new
            result.append(data)
        return result

# a = DictLoader()
# b = a.load_dicts()
