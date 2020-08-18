# -*- coding: utf-8 -*-
__author__ = 'ElenaSidorova'
import re

SYMBOLS = {
    'symbols': [u'[', u']', u'-', u"'"],
    'numbers': [u'0', u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8', u'9'],
    'brackets': [u'[', u']']
}

class WordTokenizer(object):
    @classmethod
    def tokenize(cls, text):
        tokens = []
        for litera in text:
            if not tokens:
                tokens.append(litera)
                continue
            if litera.isalpha():
                if tokens[-1][-1].isalpha():
                    tokens[-1] += litera
                elif tokens[-1][-1] in SYMBOLS['symbols']:
                    tokens[-1] += litera
                else:
                    tokens.append(litera)
                continue
            if litera in SYMBOLS['symbols']:
                if tokens[-1][-1].isalpha():
                    tokens[-1] += litera
                elif tokens[-1][-1] in SYMBOLS['symbols']:
                    if litera == u'[' and tokens[-1][-1] in SYMBOLS['brackets']:
                        tokens.append(litera)
                        continue
                    if litera == u']' and tokens[-1][-1] in SYMBOLS['brackets']:
                        tokens.append(litera)
                        continue
                    tokens[-1] += litera
                else:
                    tokens.append(litera)
                continue
            if litera in SYMBOLS['numbers']:
                if tokens[-1][-1] in SYMBOLS['numbers']:
                    tokens[-1] += litera
                else:
                    tokens.append(litera)
                continue
            tokens.append(litera)
        refactored = []
        for token in tokens:
            if u']' not in token and u'[' not in token:
                refactored.append(token)
            else:
                new = cls.check_token(token)
                if isinstance(new, str):
                    refactored.append(token)
                else:
                    refactored += new
        refactored = cls.group_brackets(refactored)
        return refactored

    @classmethod
    def group_brackets(cls, tokens):
        edited = []
        pos = 0
        for i, token in enumerate(tokens):
            if pos >= len(tokens):
                break
            if tokens[pos] == u'[':
                test_tokens = tokens[pos+1:]
                if len(test_tokens) == 0:
                    edited.append(tokens[pos])
                    pos += 1
                    continue
                ok_symb = 0
                joined = None
                arr = []
                closed = 0
                n = 0
                for j, st in enumerate(test_tokens):
                    if ok_symb > 1:
                        break
                    if not st[0].isalpha() and st[0] not in SYMBOLS['symbols']:
                        if ok_symb > 1:
                            if closed and arr:
                                arr = arr[:-1]
                                if arr:
                                    joined = 1
                            break
                        if re.search(u'^\s$', st):
                            if closed and arr:
                                joined = 1
                            break

                        else:
                            if not ok_symb:
                                ok_symb += 1
                                arr.append(st)
                            else:
                                if closed and arr:
                                    joined = 1
                                break
                    elif st == u']':
                        if closed:
                            if arr:
                                joined = 1
                            break
                        closed = 1
                        arr.append(st)
                    elif st == u'[':
                        if closed and arr:
                            joined = 1
                        break
                    else:
                        arr.append(st)
                    n += 1

                if joined and arr:
                    token = token + u''.join(arr)

                if not pos:
                    edited.append(token)
                    if joined and arr:
                        pos += n
                    pos += 1
                    continue

                if joined and arr:
                    if tokens[pos-1][-1].isalpha() or tokens[pos-1][-1] in SYMBOLS['symbols']:
                        edited[-1] += token
                    pos += n
                    pos += 1
                    continue
                else:
                    edited.append(token)
                    pos += 1

            else:
                edited.append(tokens[pos])
                pos += 1
        return edited

    @classmethod
    def check_token(cls, token):
        if u'[' in token and u']' not in token:
            token = cls.split_token(token)
        elif u']' in token and u'[' not in token:
            token = cls.split_token(token)
        elif cls.check_order_and_amount(token) is None:
            token = cls.split_token(token)
        return token

    @classmethod
    def check_order_and_amount(cls, token):
        left = []
        right = []
        for i, litera in enumerate(token):
            if litera == u'[':
                left.append(i)
            if litera == u']':
                right.append(i)
        if len(left) != len(right):
            return None
        for i, el in enumerate(left):
            if el > right[i]:
                return None
            if el + 1 == right[i]:
                return None
        return 1

    @classmethod
    def split_token(cls, token):
        arr = []
        single = []
        for i, litera in enumerate(token):
            if litera in SYMBOLS['brackets']:
                single.append(i)
                arr.append(litera)
                continue
            if i-1 >= 0 and i-1 not in single:
                if not arr:
                    arr.append(litera)
                else:
                    arr[-1] += litera
            else:
                arr.append(litera)
        return arr

# a = WordTokenizer()
# b = a.tokenize(u'''...те\nст... токенизатора.''')
# b = a.tokenize(u'обычно[мъ] своемъ мѣстѣ, подлѣ барометра, разставивъ ноги на приличное раз[стояніе], заложивъ руки назадъ и приводя за спиною пальцы въ движеніе тѣмъ быстрѣе, чѣмъ болѣе горячился [13] папа, спереди не выказывалъ ни малѣйшаго знака безпокойства, но, напротивъ, выраженіемъ лица выказывалъ совершенное сознаніе своей правоты и вмѣстѣ съ тѣмъ подвластности.')
#b = a.tokenize(u'«скоб[к»и]»')
# b = u"который [на] обычно[мъ] [своемъ] мѣстѣ, под[лѣ] баро[метра], разст[авивъ], любо[въ] 123 д'артань-ян"
# b = u'qwe[re]fs jk[]jk'
# b = u'«скоб[к»и]po» [скобки]'
# b = a.tokenize(b)
#print ('\n'.join(b))
# print u'\n'.join(a.get_tokens(b))
