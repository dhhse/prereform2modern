# -*- coding: utf-8 -*-
__author__ = 'ElenaSidorova'
import re
from copy import deepcopy

from prereform2modern.dict_settings import DictLoader


signs = [u'!', u'?', u',', u'.', u':', u')', u'(', u'«', u'»', u'“', u'”', u'-', u'–',u'`', u';', u'\\', u'/', u'@',
         u'"', u' ', u'<', u'>', u'$']
prefix = {
    re.compile(r'^воз([пткфсцчщшх].*)', flags=34):r'вос\1',
    re.compile(r'^вз([пткфсцчщшх].*)', flags=34):r'вс\1',
    re.compile(r'^низ([пткфсцчщшх].*)', flags=34):r'нис\1',
    re.compile(r'^из([пткфсцчщшх].*)', flags=34):r'ис\1',
    re.compile(r'^раз([пткфсцчщшх].*)', flags=34):r'рас\1',
    re.compile(r'^роз([пткфсцчщшх].*)', flags=34):r'рос\1',
    re.compile(r'^без([пткфсцчщшх].*)', flags=34):r'бес\1',
    re.compile(r'^через([пткфсцчщшх].*)', flags=34):r'черес\1',
    re.compile(r'^чрез([пткфсцчщшх].*)', flags=34):r'чрес\1'
}
particles = [u'б', u'бы', u'ль', u'ли', u'же', u'ж', u'ведь', u'мол', u'даже', u'дескать', u'будто']
alphabet = u'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
cyrillic = [u'ё', u'й', u'ц', u'у', u'к', u'е', u'н', u'г', u'ш', u'щ', u'з', u'х', u'ъ', u'ф', u'ы', u'в', u'а', u'п', u'р', u'о', u'л', u'д', u'ж', u'э', u'я', u'ч', u'с', u'м', u'и', u'т', u'ь', u'б', u'ю']
standard = {
    re.compile(u'^ея$', flags=34):[u'её', []],
    re.compile(u'^нея$', flags=34):[u'неё', []],
    re.compile(u'^онѣ$', flags=34):[u'они', []],
    re.compile(u'^однѣ$', flags=34):[u'одни', []],
    re.compile(u'^однѣхъ$', flags=34):[u'одних', [5]],
    re.compile(u'^однѣмъ$', flags=34):[u'одним', [5]],
    re.compile(u'^однѣми$', flags=34):[u'одними', []],
    re.compile(u'^чужаго$', flags=34):[u'чужого', []],
    re.compile(u'^пребольшаго$', flags=34):[u'пребольшого', []]
}
wrong_ends = [u'ъ', u'ъ']
old_style = {u'ѣ':u'е', u'ѳ':u'ф', u'i':u'и', u'ъи':u'ы', u'чьк':u'чк', u'чьн':u'чн', u'щию':u'щью', u'ияся':u'иеся'}
fixed_forms_exceptions = [u'благо', u'люмбаго', u'маго', u'саго']
sch_letters = [u'ч', u'щ', u'ж', u'ш']
old_style_words = {
    re.compile(r'^сватьб(.*)', flags=34):[r'свадьб\1', [], []],
    re.compile(u'^отцем$', flags=34):[u'отцом', [], []],
    re.compile(u'^найдти$', flags=34):[u'найти', [3], []],
    re.compile(u'^прийдти$', flags=34):[u'прийти', [4], []],
    re.compile(u'^перейдти$', flags=34):[u'перейти', [5], []],
    re.compile(r'^искуств(.*)', flags=34):[r'искусств\1', [], [5]],
    re.compile(u'^плечь$', flags=34):[u'плеч', [4], []],
    re.compile(u'^прогрес$', flags=34):[u'прогресс', [], [7]],
    re.compile(r'^прогреси(.*)', flags=34):[r'прогресси\1', [], [7]],
    re.compile(r'^учон(.+)', flags=34):[r'учен\1', [], []],
    re.compile(r'^внимателн(.*)', flags=34):[r'внимательн\1', [], [8]],
    re.compile(r'^оффици(.*)', flags=34):[r'офици\1', [2], []],
    re.compile(r'^симетри(.*)', flags=34):[r'симметри\1', [], [3]],
    re.compile(r'^противу(.+)', flags=34):[r'противо\1', [], []]
}
prefixed_exceptions = [
    re.compile(u'^восем.*', flags=34),
    re.compile(u'^восвояси.*', flags=34),
    re.compile(u'^низк.*', flags=34),
    re.compile(u'^низш.*', flags=34),
    re.compile(u'^возк.*', flags=34)
]
dict_settings = DictLoader.load_dicts()

class Transliterator(object):
    @classmethod
    def transliterate(cls, word, print_log=True):
        if re.search(u'^[XIVLMxivlm]+$', word):
            return word
        new_word = []
        splitted = 0
        for i, el in enumerate(word.split(u'-')):
            if el in particles:
                splitted = 1
            else:
                el = cls.convert_word(el, print_log)
            # if print_log:
            #     print('EL', el)
            new_word.append(el)
        if not splitted:
            word = u'-'.join(new_word)
        else:
            word = u' '.join(new_word)
        return word

    @classmethod
    def convert_word(cls, part, print_log=True):
        old = deepcopy(part)
        if cls.is_foreign(part):
            return part
        part, uppers = cls.get_uppers_positions(part)
        if u"'" in part:
            part, quotes = cls.get_quotes_positions(part)
            part = part.replace(u"'", u'')
        else:
            quotes = []
        if u'[' in part:
            part, left, right = cls.get_brackets_positions(part)
        else:
            left = []
            right = []
        for key in standard:
            if key.search(part):
                if standard[key][1]:
                    deleted = cls.get_new_deleted_position(standard[key][1][0], deepcopy(left), deepcopy(right), deepcopy(quotes))
                else:
                    deleted = []
                part = standard[key][0]
                if quotes:
                    if left or right:
                        if quotes[0] < left[0]:
                            part = cls.return_quotes(part, quotes, deleted, [])
                            part = cls.return_brackets(part, left, right, deleted, [])
                        else:
                            part = cls.return_brackets(part, left, right, deleted, [])
                            part = cls.return_quotes(part, quotes, deleted, [])
                            part = cls.return_brackets(part, left, right, deleted, [])
                    else:
                        part = cls.return_quotes(part, quotes, deleted, [])
                        part = cls.return_brackets(part, left, right, deleted, [])
                else:
                    part = cls.return_brackets(part, left, right, deleted, [])
                return part
        part, deleted = cls.check_old_end(part, [], [deepcopy(quotes), deepcopy(left), deepcopy(right)])
        part, newdel, added = cls.format_old_style_word(part, [quotes, left, right])
        deleted += newdel
        part = cls.replace_old_style_letters(part, print_log)
        part = cls.check_adjective_ends(part)
        if len(part) > 2:
            if part[-2:] == u'ия' or part[-2:] == u'ол':
                part = cls.check_wrong_ends(part)
        part = cls.check_prefix(part)
        if quotes:
            if left or right:
                if quotes[0] < left[0]:
                    part = cls.return_quotes(part, quotes, deleted, added)
                    part = cls.return_brackets(part, left, right, deleted, added)
                else:
                    part = cls.return_brackets(part, left, right, deleted, added)
                    part = cls.return_quotes(part, quotes, deleted, added)
                    part = cls.return_brackets(part, left, right, deleted, added)
            else:
                part = cls.return_quotes(part, quotes, deleted, added)
                part = cls.return_brackets(part, left, right, deleted, added)
        else:
            part = cls.return_brackets(part, left, right, deleted, added)
        part = cls.return_upper_positions(part, uppers, deleted, added)
        if u"''" not in old and u"''" in part:
            part = part.replace(u"''", u"'")
        return part

    @classmethod
    def get_new_deleted_position(cls, n, left, right, quotes):
        pts = [left, right, quotes]
        pts, n = cls.three_deletes(pts, n)
        pts, n = cls.three_deletes(pts, n)
        pts, n = cls.three_deletes(pts, n)
        return [n]

    @classmethod
    def three_deletes(cls, pts, n):
        for p in pts:
            for el in p:
                if el <= n:
                    n += 1
                    p.remove(el)
        return pts, n

    @classmethod
    def get_uppers_positions(cls, part):
        uppers = []
        for i, letter in enumerate(part):
            if letter.isupper():
                uppers.append(i)
        return part.lower(), uppers

    @classmethod
    def return_upper_positions(cls, part, uppers, deleted, added):
        if not uppers:
            return part
        word = u''
        position = 0
        previous = 0
        for i, letter in enumerate(part):
            if position in deleted:
                position = cls.pass_deleted_letters(position+1, deleted)
            if position in added:
                if previous and position+1 in uppers:
                    word += letter.capitalize()
                else:
                    word += letter
            if position in uppers:
                word += letter.capitalize()
                position += 1
            else:
                word += letter
                position += 1
        return word

    @classmethod
    def get_brackets_positions(cls, part):
        l = re.compile(u'\[')
        left = []
        for m in l.finditer(part):
            s = m.start()
            left.append(s)
        r = re.compile(u'\]')
        right = []
        for m in r.finditer(part):
            s = m.start()
            right.append(s)
        part = part.replace(u'[', u'')
        part = part.replace(u']', u'')
        return part, left, right

    @classmethod
    def get_quotes_positions(cls, part):
        q = re.compile(u"'")
        quotes = []
        for m in q.finditer(part):
            s = m.start()
            quotes.append(s)
        return part, quotes

    @classmethod
    def return_brackets(cls, part, left, right, deleted, added):
        position = 0
        word = u''
        for i, letter in enumerate(part):
            if position in deleted:
                position = cls.pass_deleted_letters(position+1, deleted)
            if position in added:
                word += letter
                continue
            word, position = cls.add_left_bracket(position, left, right, word, deleted)
            word, position = cls.add_right_bracket(position, left, right, word, deleted)
            word += letter
            position += 1
        word, position = cls.add_left_bracket(position, left, right, word, deleted)
        word, position = cls.add_right_bracket(position, left, right, word, deleted)
        return word

    @classmethod
    def return_quotes(cls, part, quotes, deleted, added):
        position = 0
        word = u''
        for i, letter in enumerate(part):
            if position in deleted:
                position = cls.pass_deleted_letters(position+1, deleted)
            if position in added:
                word += letter
                continue
            word, position = cls.add_quote(position, quotes, word, deleted)
            word += letter
            position += 1
        word, position = cls.add_quote(position, quotes, word, deleted)
        return word

    @classmethod
    def add_quote(cls, position, quotes, word, deleted):
        if position in deleted:
            position = cls.pass_deleted_letters(position+1, deleted)
        if position in quotes:
            word += u"'"
            position += 1
            word, position = cls.add_quote(position, quotes, word, deleted)
        else:
            return word, position
        return word, position

    @classmethod
    def add_left_bracket(cls, position, left, right, word, deleted):
        if position in deleted:
            position = cls.pass_deleted_letters(position+1, deleted)
        if position in left:
            word += u'['
            left.remove(position)
            position += 1
            word, position = cls.add_right_bracket(position, left, right, word, deleted)
            word, position = cls.add_left_bracket(position, left, right, word, deleted)
        else:
            return word, position
        return word, position

    @classmethod
    def add_right_bracket(cls, position, left, right, word, deleted):
        if position in deleted:
            position = cls.pass_deleted_letters(position+1, deleted)
        if position in right:
            word += u']'
            right.remove(position)
            position += 1
            word, position = cls.add_left_bracket(position, left, right, word, deleted)
            word, position = cls.add_right_bracket(position, left, right, word, deleted)
        else:
            return word, position
        return word, position

    @classmethod
    def pass_deleted_letters(cls, p, deleted):
        if p in deleted:
            p = cls.pass_deleted_letters(p+1, deleted)
        else:
            return p
        return p

    @classmethod
    def format_old_style_word(cls, part, pos):
        for key in old_style_words.keys():
            new = re.sub(key, old_style_words[key][0], part)
            if part != new:
                newdel = []
                for n in old_style_words[key][1]:
                    pos, n = cls.three_deletes(pos, n)
                    pos, n = cls.three_deletes(pos, n)
                    pos, n = cls.three_deletes(pos, n)
                    newdel.append(n)
                added = []
                for n in old_style_words[key][2]:
                    pos, n = cls.three_deletes(pos, n)
                    pos, n = cls.three_deletes(pos, n)
                    pos, n = cls.three_deletes(pos, n)
                    added.append(n)
                return new, newdel, added
        return part, [], []

    @classmethod
    def replace_old_style_letters(cls, part, print_log=True):
        for key in old_style:
            part = part.replace(key, old_style[key])
            # if print_log:
            #     print(key, old_style[key], part)
        return part

    @classmethod
    def check_old_end(cls, part, deleted, pos):
        # print part, part[-1]
        if part[-1] in wrong_ends:
            n = len(part) - 1
            pts, n = cls.three_deletes(pos, n)
            pts, n = cls.three_deletes(pos, n)
            pts, n = cls.three_deletes(pos, n)
            deleted.append(n)
            return part[:-1], deleted
        return part, deleted

    @classmethod
    def is_foreign(cls, part):
        part = part.lower()
        for el in part:
            if el in cyrillic:
                return 0
        return 1

    @classmethod
    def check_adjective_ends(cls, part):
        if part in fixed_forms_exceptions:
            return part
        if len(part) <= 3:
            return part
        if part[-3:] == u'аго':
            if part[-4] in sch_letters:
                return u''.join([part[:-3], u'его'])
            else:
                return u''.join([part[:-3], u'ого'])
        elif part[-3:] == u'яго':
            return u''.join([part[:-3], u'его'])
        elif part[-2:] == u'ыя':
            return u''.join([part[:-2], u'ые'])
        elif part[-2] == u'iя' and not cls.is_foreign(part):
            return cls.check_and_replace_ija_end(part)
        return part

    @classmethod
    def check_and_replace_ija_end(cls, part):
        test = part[:-2] + u'ие'
        if cls.is_in_dictionary(test):
            return part[:-2] + u'ия'
        else:
            test = part[:-2] + u'ия'
            if cls.is_in_dictionary(test) or cls.check_right_ends(test):
                return test
            else:
                return part[:-2] + u'ие'
        return part

    @classmethod
    def is_in_dictionary(cls, part):
        for d in dict_settings[0]:
            if part in d:
                return 1
        return 0

    @classmethod
    def check_wrong_ends(cls, part):
        dd = dict_settings
        for i, d in enumerate(dict_settings[1]):
            if not i:
                if len(part) > 1 and part in d:
                    part = part[:-1] + u'е'
                    return part
                else:
                    for p in dict_settings[3][0]:
                        if len(part) > len(p):
                            if part[:len(p)] == p:
                                new = part[len(p):]
                                if new in d:
                                    return part[:-1] + u'е'
            else:
                if len(part) > 2 and part in d:
                    part = part[:-2] + u'ел'
                else:
                    for p in dict_settings[3][0]:
                        if len(part) > len(p):
                            if part[:len(p)] == p:
                                new = part[len(p):]
                                if new in d:
                                    return part[:-2] + u'ел'
        return part

    @classmethod
    def check_right_ends(cls, part):
        for i, d in enumerate(dict_settings[2]):
            if part in d:
                return 1
        return 0

    @classmethod
    def check_prefix(cls, part):
        for el in prefixed_exceptions:
            if el.search(part):
                return part
        for key in prefix:
            new = re.sub(key, prefix[key], part)
            if new != part:
                return new
        return part

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
