# Prereform2modern
#### Преобразует текст из дореформенной орфографии в современную. Работает в Py3.
---
### &emsp;&emsp;Установка
```python
pip install prereform2modern
```

### &emsp;&emsp;Запуск из командной строки:
&emsp;Длинный способ
```python
python -m prereform2modern.translit_from_string "Онъ стоялъ подлѣ письменнаго стола"
```
```
Он стоял подле письменного стола
```

&emsp;Короткий способ
```python
translit "Онъ стоялъ подлѣ письменнаго стола"
```

&emsp;Флаг __-t__ отображает изменённые слова в старой орфографии.
```python
translit -t "Онъ стоялъ подлѣ письменнаго стола"
```

```python
Он{Онъ} стоял{стоялъ} подле{подлѣ} письменного{письменнаго} стола
```

### &emsp;&emsp;Запуск из интерпретатора:
```python
from prereform2modern import Processor
```
```python
orig_text = "Онъ стоялъ подлѣ письменнаго стола"
```

```python
text_res, changes, s_json = Processor.process_text(
    text=orig_text,
    show=False,
    delimiters=False,
    check_brackets=False
    )
```

### &emsp;&emsp;Выдача
* __text_res: str__

&emsp;Преобразованный текст.

```python
print(text_res)
```
```
Он стоял подле письменного стола
```

* __changes: str__

&emsp;Произведенные изменения.

```python
print(changes)
```
```
Онъ --> Он
стоялъ --> стоял
подлѣ --> подле
письменнаго --> письменного
```

* __str_json: str__

&emsp;Сведения о всех словах и символах в формате json.

```python
import json
json.loads(s_json)
```
```python
{'0': {'old_word': 'Онъ', 'type': 'word', 'word': 'Он'},
'1': {'old_word': '', 'type': 'punct', 'word': ' '},
'2': {'old_word': 'стоялъ', 'type': 'word', 'word': 'стоял'},
'3': {'old_word': '', 'type': 'punct', 'word': ' '},
'4': {'old_word': 'подлѣ', 'type': 'word', 'word': 'подле'},
'5': {'old_word': '', 'type': 'punct', 'word': ' '},
'6': {'old_word': 'письменнаго', 'type': 'word', 'word': 'письменного'},
'7': {'old_word': '', 'type': 'punct', 'word': ' '},
'8': {'old_word': '', 'type': 'word', 'word': 'стола'}}
```


### &emsp;&emsp;Параметры
```python
method Processor.process_text(
    text, show, delimiters, check_brackets
    )
```
* __text: str__

&emsp;Оригинальный текст в дореформенной орфографии.

* __show: boolean__

&emsp;Включает в результат заменённые слова в дореформенной орфографии. Если параметр `check_brackets=True`, то заменённые слова показываются при любом значении параметра show.

* __delimiters: list из трех элементов типа str__

&emsp;Используется для обозначения заменённых слов. Первый элемент помещается перед новым словом, а другие два элемента выделяют заменённое слово. Так, можно использовать скобки:
```python
delimiters=['', '{', '}']
text="примеръ"
```
```python
пример{примеръ}
```

&emsp;Или, например, теги XML (про использование тега \<choice> см. [здесь](https://en.wikipedia.org/wiki/Text_Encoding_Initiative#Choice_tag)):
```python
delimiters=['<choice><reg>', '</reg><orig>', '</orig></choice>']
```
```python
<choice><reg>пример</reg><orig>примеръ</orig></choice>
```

* __check_brackets: boolean__

&emsp;Помечает редакторскую правку.
```python
text='Пройдя комнату, такъ [называемую], офиціанскую'
delimiters=['', '{', '}']
check_brackets=True
```
```python
Пройдя комнату, так{такъ} <choice original_editorial_correction='[называемую]'><sic></sic>
<corr>называемую</corr></choice>, официанскую{офицiанскую}
```
