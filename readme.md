## Использование программы из командной строки

```
$ python2.7 prereform2modern/translit_from_string.py "Онъ стоялъ подлѣ письменнаго стола"

['prereform2modern/translit_from_string.py', '\xd0\x9e\xd0\xbd\xd1\x8a \xd1\x81\xd1\x82\xd0\xbe\xd1\x8f\xd0\xbb\xd1\x8a \xd0\xbf\xd0\xbe\xd0\xb4\xd0\xbb\xd1\xa3 \xd0\xbf\xd0\xb8\xd1\x81\xd1\x8c\xd0\xbc\xd0\xb5\xd0\xbd\xd0\xbd\xd0\xb0\xd0\xb3\xd0\xbe \xd1\x81\xd1\x82\xd0\xbe\xd0\xbb\xd0\xb0']

/Users/alexskrn/Documents/NLP/HSE/praktika/prereform2modern/prereform2modern/word_tokenize.py:27: UnicodeWarning: Unicode equal comparison failed to convert both arguments to Unicode - interpreting them as being unequal
  if litera in SYMBOLS['symbols']:
/Users/alexskrn/Documents/NLP/HSE/praktika/prereform2modern/prereform2modern/word_tokenize.py:41: UnicodeWarning: Unicode equal comparison failed to convert both arguments to Unicode - interpreting them as being unequal
  if litera in SYMBOLS['numbers']:

Он{Онъ} стоял{стоялъ} подле{подлѣ} письменного{письменнаго} стола
```

Флаг __-t__ позволяет получить результат в формате __json__
```
$ python2.7 prereform2modern/translit_from_string.py -t "Онъ"

{"0": {"type": "word", "old_plain_word": null, "word": "\u041e\u043d", "old_word": "\u041e\u043d\u044a", "plain_word": null}}
```

Как это должно работать в Py3:
```
$ python3 prereform2modern/translit_from_string.py "Онъ"

['prereform2modern/translit_from_string.py', 'Онъ']

Он{Онъ}
```
В Py3 кажется сохраняется проблема с юникодом в объекте json:
```
$ python3 prereform2modern/translit_from_string.py -t "Онъ"

['prereform2modern/translit_from_string.py', '-t', 'Онъ']

{"0": {"word": "\u041e\u043d", "old_word": "\u041e\u043d\u044a", "type": "word", "plain_word": null, "old_plain_word": null}}
```

## Использование программы из интерпретатора

Программа из интерпретатора запускается так:
```
$ python2.7
>>> from process import Processor
>>> text = u'офицiанскую'  # например
>>> t, change, w_edits, _json = Processor.process_text(text, show=False, delimiters=[u'', u'{', u'}'], check_brackets=False, print_log=False)
>>> print t
официанскую
```

<hr>
method Processor.process_text(text, show, delimiters, check_brackets, print_log=True)
<hr>

Используется для преобразования текста в дореформенной орфографии в текст в современной орфографии.


Parameters: __text: unicode__

Оригинальный текст в дореформенной орфографии

__show: boolean__

Используется для обозначения того, будут ли в результат включены слова в дореформенной орфографии, которые были заменены. Если параметр check_brackets=True, то замененные слова в любом случае показываются, независимо от значения параметра show.

__delimiters: list из трех элементов типа unicode__

Используется для обозначения замененных слов. Первый элемент помещается перед новым словом, а вторые два элемента выделяют замененное слово. Например, если
```
delimiters=[u'', u'{', u'}'], text=u"примеръ"
```
то результат будет
```
пример{примеръ}
```

Если
```
delimiters=[u'<choice><reg>', u'</reg><orig>', u'</orig></choice>']
```
то результат будет
```
<choice><reg>пример</reg><orig>примеръ</orig></choice>
```

КОМУ МОЖЕТ ПОТРЕБОВАТЬСЯ ПОСЛЕДНИЙ ВАРИАНТ? ПРО ТАКОЙ ФОРМАТ, ГОВОРИТСЯ, НАПРИМЕР, ВОТ ЗДЕСЬ: https://en.wikipedia.org/wiki/Text_Encoding_Initiative#Choice_tag

__check_brackets: boolean__

Используется для обозначения в преобразованном тексте редакторской правки в оригинале текста. Например, если  text=u'Пройдя комнату, такъ [называемую], офиціанскую', delimiters=[u'', u'{', u'}'], check_brackets=True, то результат будет следующим:
```
Пройдя комнату, так{такъ} <choice original_editorial_correction='[называемую]'><sic></sic><corr>называемую</corr></choice>, официанскую{офицiанскую}
```

ЗДЕСЬ ТОТ ЖЕ ВОПРОС, ЧТО И ВЫШЕ - ЗАЧЕМ МОЖЕТ БЫТЬ НУЖНО ТАКОЕ ФОРМАТИРОВАНИЕ?

__print_log: boolean__

КАК ОПИСАТЬ, ЧТО ПОКАЗЫВАЕТ ЛОГ? В КАКОЙ ПОСЛЕДОВАТЕЛЬНОСТИ ПРОВЕРЯЕТСЯ НАЛИЧИЕ СПЕЦИАЛЬНЫХ СИМВОЛОВ И В КАКОЙ ОНИ ЗАМЕНЯЮТСЯ?

Примеры такие, если print_log=True, а text = u'офицiанскую', то на печать выводится следующее:
```
ѣ е офицiанскую
чьк чк офицiанскую
ъи ы офицiанскую
чьн чн офицiанскую
ияся иеся офицiанскую
i и официанскую
щию щью официанскую
ѳ ф официанскую
EL официанскую
````

Если text=u'выраженіемъ', то на печать выводится вот это:

```
ѣ е выраженiем
чьк чк выраженiем
ъи ы выраженiем
чьн чн выраженiем
ияся иеся выраженiем
i и выражением
щию щью выражением
ѳ ф выражением
EL выражением
```

Returns: __text: unicode__

Преобразованный текст

__changes: unicode__

Произведенные изменения в виде "офицiанскую --> официанскую"

__wrong_edits: list__

ВСЕ ВРЕМЯ ПУСТОЙ СПИСОК, НЕ ЯСНО, ЧТО ТАМ МОЖЕТ БЫТЬ. ПРИМЕРОВ НЕТ

__str_json: str__

Например, если text=u'офицiанскую', то str_json =
```
'{"0": {"type": "word", "old_plain_word": null, "word": u"официанскую", "old_word": u"офицiанскую", "plain_word": null}}'
```

ЧТО ОЗНАЧАЮТ КЛЮЧИ OLD_PLAIN_WORD И PLAIN_WORD? ВО ВСЕХ ПРИМЕРАХ ЗНАЧЕНИЯ ЭТИХ КЛЮЧЕЙ = NULL. МОЖЕТ БЫТЬ, ЕСЛИ ВЗЯТЬ БОЛЬШЕ ПРИМЕРОВ ТЕКСТА ИЗ ТОГО XML-ФАЙЛА, ЧТО ПРИСЫЛАЛ ДАНИИЛ, ТО МОЖНО НАЙТИ ПРИМЕР, КОГДА ИХ ЗНАЧЕНИЕ НЕ РАВНО NULL, И ТОГДА МОЖНО БЫЛО БЫ ПОНЯТЬ, ЧТО ТАКОЕ OLD_PLAIN_WORD И PLAIN_WORD?  
