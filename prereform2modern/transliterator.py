# -*- coding: utf-8 -*-
__author__ = 'ElenaSidorova'

class Transliterator(object):
    def transliterate(self, fake_para):
        return u'Он'


# a = Transliterator()
# b = a.return_brackets(u'внимательно', [3], [5], [], [10])
# b = a.transliterate(u"б[езпроизошол'ъ']")
# b = a.transliterate(u"без'произошол")
# b = a.transliterate(u"жилъ-бы")
# b = a.transliterate(u'выраженіемъ')
#без'произошол безпроизошол")
# b = a.check_old_end(u'привет', [])
# print b
# b = a.return_upper_positions(b, [0,1,7], [1])
# b = a.is_foreign(u'hello')
# print b
