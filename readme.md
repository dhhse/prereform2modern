# Prereform2modern
#### Преобразует текст из дореформенной орфографии в современную.  
---
### &emsp;&emsp;Использование программы из командной строки в Py3:

```python
$ python3 prereform2modern/translit_from_string.py "Онъ стоялъ подлѣ письменнаго стола"
```

```python

Он стоял подле письменного стола
```

&emsp;Флаг __-t__ позволяет получить результат в формате __json__
```python
$ python3 prereform2modern/translit_from_string.py -t "Онъ стоялъ подлѣ письменнаго стола"
```

```python

Он{Онъ} стоял{стоялъ} подле{подлѣ} письменного{письменнаго} стола
```

---
### &emsp;&emsp;Использование программы из интерпретатора


```python
$ python3
>>> from process import Processor
>>> text = u'офицiанскую'  # например
>>> t, change, w_edits, _json = Processor.process_text(text, show=False, delimiters=[u'', u'{', u'}'],
check_brackets=False, print_log=False)
>>> print t
```
```
официанскую
```

### &emsp;&emsp;Параметры
```python
method Processor.process_text(text, show, delimiters, check_brackets, print_log=True)
```
* __text: unicode__

&emsp;Оригинальный текст в дореформенной орфографии.

* __show: boolean__

&emsp;Включает в результат заменённые слова в дореформенной орфографии. Если параметр `check_brackets=True`, то заменённые слова показываются при любом значении параметра show.

* __delimiters: list из трех элементов типа unicode__

&emsp;Используется для обозначения заменённых слов. Первый элемент помещается перед новым словом, а вторые два элемента выделяют заменённое слово. Так, можно использовать скобки:
```python
delimiters=[u'', u'{', u'}']
text=u"примеръ"
```
```python
пример{примеръ}
```

&emsp;Или, например, теги XML (про использование тега \<choice> см. [здесь](https://en.wikipedia.org/wiki/Text_Encoding_Initiative#Choice_tag)):
```python
delimiters=[u'<choice><reg>', u'</reg><orig>', u'</orig></choice>']
```
```python
<choice><reg>пример</reg><orig>примеръ</orig></choice>
```

* __check_brackets: boolean__

&emsp;Помечает редакторскую правку.
```python
text=u'Пройдя комнату, такъ [называемую], офиціанскую'
delimiters=[u'', u'{', u'}']
check_brackets=True
```
```python
Пройдя комнату, так{такъ} <choice original_editorial_correction='[называемую]'><sic></sic>
<corr>называемую</corr></choice>, официанскую{офицiанскую}
```

* __print_log: boolean__

&emsp;Отображает замены, которые выполняет программа. Через пробел: символ старой орфографии, символ новой орфографии, слово после замены.
```python
print_log=True
```
```python
text=u'офицiанскую'
```
```python
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

```python
text=u'выраженіемъ'
```

```python
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

### &emsp;&emsp;Выдача
* __text: unicode__

&emsp;Преобразованный текст.

* __changes: unicode__

&emsp;Произведенные изменения в виде "офицiанскую --> официанскую".


* __str_json: str__
```python
text=u'офицiанскую'
```
```python
'{"0": {"type": "word", "old_plain_word": null, "word": u"официанскую", "old_word": u"офицiанскую",
"plain_word": null}}'
```
