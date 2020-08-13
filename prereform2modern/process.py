# -*- coding: utf-8 -*-
__author__ = 'ElenaSidorova'
from copy import deepcopy
import json
# import subprocess

from prereform2modern.preprocess import Preprocessor
from prereform2modern.tokenizer import Tokenizer
from prereform2modern.transliterator import Transliterator
from prereform2modern.meta_data import META


class Processor(object):
    @classmethod
    def process_text(cls, text, show, delimiters, check_brackets):
        text = Preprocessor.preprocess_text(text)
        tokens = Tokenizer.tokenize(text)
        for i in tokens.keys():
            if tokens[i].type == 'word':
                word = Transliterator.transliterate(tokens[i].word, print_log=False)
                if word != tokens[i].word:
                    tokens[i].old_word = deepcopy(tokens[i].word)
                    tokens[i].word = word
        text, changes = cls.join_tokens(tokens, show, delimiters, check_brackets)
        str_json = cls.to_json(tokens)
        return text, changes, str_json

    @classmethod
    def to_json(cls, tokens):
        jn = {}
        for key in tokens.keys():
            jn[str(key)] = {}
            jn[str(key)]['word'] = tokens[key].word
            jn[str(key)]['old_word'] = tokens[key].old_word
            jn[str(key)]['type'] = tokens[key].type
            # jn[str(key)]['plain_word'] = tokens[key].plain_word
            # jn[str(key)]['old_plain_word'] = tokens[key].old_plain_word
        str_json = json.dumps(jn)
        return str_json

    @classmethod
    def join_tokens(cls, tokens, show, delimiters, check_brackets):
        text = []
        changes = []
        spelling = []
        # wrong_changes = []
        for i in range(len(tokens.keys())):
            if check_brackets:
                if u'[' in tokens[i].word and tokens[i].type == 'word':
                    new = u''
                    new += META['spelling_delimiters_upd'][0]
                    if tokens[i].old_word:
                        new += tokens[i].old_word.replace(u"'", u"&apos;")
                    else:
                        new += tokens[i].word.replace(u"'", u"&apos;")
                    new += META['spelling_delimiters_upd'][1]
                    if tokens[i].old_word:
                        new_vers = tokens[i].word.split(u'[')[1].split(u']')[0]
                        old_vers = tokens[i].old_word.split(u'[')[1].split(u']')[0]
                        if new_vers == old_vers:
                            new = new + tokens[i].word.split(u'[')[0] + tokens[i].word.split(u']')[1] + \
                              META['spelling_delimiters_upd'][2] + tokens[i].word.replace(u'[', u'').replace(u']', u'') + \
                              META['spelling_delimiters_upd'][3]
                        else:
                            new_spell = tokens[i].word.split(u'[')[0] + tokens[i].word.split(u']')[1]
                            old_spell = tokens[i].old_word.split(u'[')[0] + tokens[i].old_word.split(u']')[1]
                            if new_spell == old_spell:
                                new = new + tokens[i].word.split(u'[')[0] + tokens[i].word.split(u']')[1] + \
                                    META['spelling_delimiters_upd'][2] + delimiters[0] + \
                                    tokens[i].word.replace(u'[', u'').replace(u']', u'') + delimiters[1] + \
                                    tokens[i].old_word.replace(u'[', u'').replace(u']', u'') + delimiters[2] + \
                                    META['spelling_delimiters_upd'][3]
                            else:
                                new = new + delimiters[0] + tokens[i].word.split(u'[')[0] + tokens[i].word.split(u']')[1] + \
                                    delimiters[1] + tokens[i].old_word.split(u'[')[0] + tokens[i].old_word.split(u']')[1] + \
                                    delimiters[2] + META['spelling_delimiters_upd'][2] + delimiters[0] + \
                                    tokens[i].word.replace(u'[', u'').replace(u']', u'') + delimiters[1] + \
                                    tokens[i].old_word.replace(u'[', u'').replace(u']', u'') + delimiters[2] + \
                                    META['spelling_delimiters_upd'][3]
                    else:
                        new = new + tokens[i].word.split(u'[')[0] + tokens[i].word.split(u']')[1] + \
                              META['spelling_delimiters_upd'][2] + tokens[i].word.replace(u'[', u'').replace(u']', u'') + \
                              META['spelling_delimiters_upd'][3]
                    text.append(new)
                    if tokens[i].old_word:
                        spelling.append(tokens[i].word.replace(u'[', u'').replace(u']', u''))
                        s = tokens[i].old_word + u' --> ' + tokens[i].word
                        changes.append(s)
                else:
                    if tokens[i].old_word:
                        new = delimiters[0] + tokens[i].word + delimiters[1] + \
                              tokens[i].old_word + delimiters[2]
                        text.append(new)
                        spelling.append(tokens[i].word)
                        s = tokens[i].old_word + u'\t-->\t' + tokens[i].word
                        changes.append(s)
                    else:
                        text.append(tokens[i].word)

            else:
                if tokens[i].old_word:
                    if show:
                        new = delimiters[0] + tokens[i].word + delimiters[1] + \
                              tokens[i].old_word + delimiters[2]
                    else:
                        new = tokens[i].word
                    text.append(new)
                    s = tokens[i].old_word + u' --> ' + tokens[i].word
                    changes.append(s)
                else:
                    text.append(tokens[i].word)
        # if spelling:
        #     cmd = "echo " + u' '.join(spelling) + " | hunspell -d ru_Ru"
        #     p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, executable="/bin/bash")
        #     spelled, err_sp = p.communicate()
        #     spelled = spelled.split('\n')[1:][:-2]
        #     for j, sp in enumerate(spelled):
        #         if sp [0] == u'&':
        #             wrong_changes.append(changes[j])
        #             changes[j] = changes[j] + u' *'
        if changes == []:
            out = u''
        else:
            out = u'\n'.join(changes)
        return u''.join(text), out


# text = u'Пройдя комнату, такъ [называемую], офиціанскую, мы взошли въ кабинетъ Папа. Онъ стоялъ подлѣ письменнаго стола и, показывая на бумаги, запечатанные конверты, кучки денегъ, горячился и что-то толковалъ прикащику Никитѣ Петрову, который на обычно[мъ] своемъ мѣстѣ, подлѣ барометра, разставивъ ноги на приличное раз[стояніе], заложивъ руки назадъ и приводя за спиною пальцы въ движеніе тѣмъ быстрѣе, чѣмъ болѣе горячился [13] папа, спереди не выказывалъ ни малѣйшаго знака безпокойства, но, напротивъ, выраженіемъ лица выказывалъ совершенное сознаніе своей правоты и вмѣстѣ съ тѣмъ подвластности.'
# text = u'df 13 fsdf'
# text = u'офиціанскую'
# text = u' обычно[мъ] '
# text = u'который [на] обычно[мъ] [своемъ] мѣстѣ, под[лѣ] баро[метра], разст[авивъ], любо[въ]'
# import codecs
# with codecs.open(u'/Users/el/Downloads/vol. 1/index.html', 'r', 'utf-8') as inf:
#     text = inf.read()
# a = Processor()
# b, c, r, m = a.process_text(text, 1, [u'<choice><reg>', u'</reg><orig>', u'</orig></choice>'], 1)
# print b
