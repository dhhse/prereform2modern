# -*- coding: utf-8 -*-
__author__ = 'ElenaSidorova'
import re
from copy import deepcopy

from prereform2modern.token_class import Token
from prereform2modern.word_tokenize import WordTokenizer


class Tokenizer(object):
    @classmethod
    def tokenize(cls, text):
        """
        Tokenizes the text
        :param text: the raw text
        :return: tokens (dict format)
        """
        tokens = {}
        parts = WordTokenizer.tokenize(text)
        current = 0
        id = 0
        for i, part in enumerate(parts):
            tokens[i] = Token(part)
            current += len(part)
            id += 1
        tokens = cls.get_types(tokens)
        return tokens

    @classmethod
    def refactor(cls, tokens):
        """
        Joins the tokens with the brackets []
        :param tokens: the tokens (dict)
        :return: the refactored tokens
        """
        ref = {}
        j = 0
        for i in range(len(tokens.keys())):
            if tokens[i].word == u'[':
                if tokens.has_key(i + 1):
                    if tokens[i + 1].word == u'?':
                        ref[j] = tokens[i]
                        i += 1
                        j += 1
                    else:
                        if ref.has_key(j-1):
                            if ref[j-1].type == u'word':
                                ref[j-1].word = ref[j-1].word + u'['
                                i += 1
                            else:
                                ref[j] = tokens[i]
                                i += 1
                                j += 1
                        else:
                            ref[j] = tokens[i]
                            i += 1
                            j += 1
                else:
                    ref[j] = tokens[i]
                    i += 1
                    j += 1
            elif tokens[i].word == u'?':
                if ref.has_key(j-1):
                    if ref[j-1].word == u'[':
                        ref[j-1].word = ref[j-1].word + u'?'
                        i += 1
                    else:
                        ref[j] = tokens[i]
                        i += 1
                        j += 1
                else:
                    ref[j] = tokens[i]
                    i += 1
                    j += 1
            elif tokens[i].word == u']':
                if ref.has_key(j-1):
                    if ref[j-1].word == u'[?':
                        ref[j-1].word = ref[j-1].word + u']'
                        i += 1
                    else:
                        if ref[j-1].type == u'word':
                            if u'[' in ref[j-1].word and u']' not in ref[j-1].word:
                                ref[j-1].word = ref[j-1].word + u']'
                                i += 1
                            else:
                                ref[j] = tokens[i]
                                i += 1
                                j += 1
                        else:
                            ref[j] = tokens[i]
                            i += 1
                            j += 1
                else:
                    ref[j] = tokens[i]
                    i += 1
                    j += 1
            else:
                if ref.has_key(j-1):
                    if len(ref[j-1].word) > 1 and ref[j-1].word[-1] == u'[' and tokens[i].type == 'word':
                        ref[j-1].word = ref[j-1].word + tokens[i].word
                        i += 1
                    elif len(ref[j-1].word) > 1 and ref[j-1].word[-1] == u']' and tokens[i].type == 'word':
                        ref[j-1].word = ref[j-1].word + tokens[i].word
                        i += 1
                    else:
                        ref[j] = tokens[i]
                        i += 1
                        j += 1
                else:
                    ref[j] = tokens[i]
                    i += 1
                    j += 1
        out = {}
        k = 0
        for j in range(len(ref.keys())):
            k, out, added = cls.split_passed(j, k, ref, out, u'[', u']')
            if not added:
                k, out, added = cls.split_passed(j, k, ref, out, u']', u'[')
                if not added:
                    out[k] = ref[j]
                    k += 1
        return out

    @classmethod
    def split_passed(cls, j, k, ref, out, symbol1, symbol2):
        added = 0
        if symbol1 in ref[j].word:
            if symbol2 in ref[j].word:
                out[k] = ref[j]
                k += 1
                return k, out, 1
            else:
                tmp = deepcopy(ref[j])
                arr = cls.get_tmp_arr(ref[j].word.split(symbol1), symbol1)
                for el in arr:
                    tmp.word = el
                    out[k] = deepcopy(tmp)
                    k += 1
                added = 1
        return k, out, added

    @classmethod
    def get_tmp_arr(cls, tmpar, symbol):
        arr = []
        for i, el in enumerate(tmpar):
            if i >= len(tmpar) - 1:
                if el != u'':
                    arr.append(el)
                continue
            if el != u'':
                arr.append(el)
            arr.append(symbol)
        return arr

    @classmethod
    def add_space_symbols(cls, current, new_lines, tokens, id, res, spaces):
        """
        Adds the spaces by the list of positions
        :param current: the number of the current letter
        :param new_lines: the list of the new lines positions \n
        :param tokens: the tokens
        :param id: the number of the part of the text
        :param res: the list of the \r positions
        :param spaces: the list of the spaces positions
        :return: the new current position, the tokens, the number of the part
        """
        current, tokens, id = cls.add_new_lines(current, new_lines, tokens, id, res, spaces)
        current, tokens, id = cls.add_r_lines(current, res, tokens, id, spaces, new_lines)
        current, tokens, id = cls.add_spaces(current, spaces, tokens, id, new_lines, res)
        return current, tokens, id

    @classmethod
    def add_new_lines(cls, current, new_lines, tokens, id, res, spaces):
        """
        Adds the new lines by the list of positions
        :param current: the number of the current letter
        :param new_lines: the list of the new lines positions \n
        :param tokens: the tokens
        :param id: the number of the part of the text
        :param res: the list of the \r positions
        :param spaces: the list of the spaces positions
        :return: the new current position, the tokens, the number of the part
        """
        if current in new_lines:
            tokens[id] = Token(u'\n')
            id += 1
            current += 1
            current, tokens, id = cls.add_r_lines(current, res, tokens, id, spaces, new_lines)
            current, tokens, id = cls.add_spaces(current, spaces, tokens, id, new_lines, res)
            current, tokens, id = cls.add_new_lines(current, new_lines, tokens, id, res, spaces)
        return current, tokens, id

    @classmethod
    def add_r_lines(cls, current, res, tokens, id, spaces, new_lines):
        """
        Adds the \r by the list of positions
        :param current: the number of the current letter
        :param res: the list of the \r positions
        :param tokens: the tokens
        :param id: the number of the part of the text
        :param spaces: the list of the spaces positions
        :param new_lines: the list of the new lines positions \n
        :return: the new current position, the tokens, the number of the part
        """
        if current in res:
            tokens[id] = Token(u'\r')
            id += 1
            current += 1
            current, tokens, id = cls.add_spaces(current, spaces, tokens, id, new_lines, res)
            current, tokens, id = cls.add_new_lines(current, new_lines, tokens, id, res, spaces)
            current, tokens, id = cls.add_r_lines(current, res, tokens, id, spaces, new_lines)
        return current, tokens, id

    @classmethod
    def add_spaces(cls, current, spaces, tokens, id, new_lines, res):
        if current in spaces:
            tokens[id] = Token(u' ')
            id += 1
            current += 1
            current, tokens, id = cls.add_new_lines(current, new_lines, tokens, id, res, spaces)
            current, tokens, id = cls.add_r_lines(current, res, tokens, id, spaces, new_lines)
            current, tokens, id = cls.add_spaces(current, spaces, tokens, id, new_lines, res)
        return current, tokens, id

    @classmethod
    def get_types(cls, tokens):
        for t in tokens.keys():
            w = 0
            for letter in tokens[t].word:
                if letter.isalpha():
                    tokens[t].type = 'word'
                else:
                    w += 1
            if w == len(tokens[t].word):
                tokens[t].type = 'punct'
            if tokens[t].type == None:
                tokens[t].type = 'word'
        return tokens

# t = u'\n \r\r\r \n \r \n\n\n \r \n yuy ghjg werwer-er по-моему?'
# t = u'мам[а]м'
# t = u'это всего [лишь скоб[к]и]'
# t = u'«скоб[к»и]» [скобки]'
# t = u'"Да не по горамъ-горамъ"'
# a = Tokenizer()
# b = a.tokenize(t)
# c = a.refactor(b)
# print c
# print b
# print u'\n'.join(b)
