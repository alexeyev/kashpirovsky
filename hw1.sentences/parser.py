# -*- coding: utf-8 -*-
"""
Деление текста на русском языке на предложения.
На вход в качестве параметра подаются два файла:
1 входной текстовый
2 файл для вывода результата в формате:
<?xml version="1.0" encoding="UTF-8" ?>
<sentences>
<sentence>Предложение1</sentence>
<sentence>Предложение2</sentence>
</sentences>

author: kashpirovsky team

"""

import re, sys

# todo: move patterns to global variables

"""
Ниже -- список предикатов, проверяющих некоторые условия для данной позиции в тексте.
С их помощью и производится разделение на предложения. Список можно пополнять, добавляя
новые предикаты в [fpatterns].
"""

def is_end(pos, par):
    return pos == len(par) - 1

def basic(position, par):
    """Заканчивается на точку, вопросительный или восклицательный знаки и пробел"""
    return re.match("^[\.\?!] $",par[position - 1 : position + 1]) is not None

def prev_capital(position, par):
    """На 2 позиции до рассматриваемой стоит заглавная буква."""
    return re.match(u"[A-ZА-Я]",par[position - 2: position - 1]) is not None

def next_capital(position, par):
    """Следующая -- заглавная (+ basic + не prev_capital)"""
    return basic(position, par) and not prev_capital(position, par) and re.match(u" [A-ZА-Я0-9]",par[position : position + 2]) is not None 

def check_shortenings(pos, par):
    """Перед точкой -- не скоращение из 1-2 букв"""
    return next_capital(pos, par) and re.match(u".* [a-zа-я]{1,2}\. $", par[pos - 5 : pos + 1]) is None

def num(pos, par):
    """После числа -- точка и пробел; кажется, это всегда признак конца предложения"""
    return re.match(u"[0-9][\\.\\?!]+ $",par[pos - 5 : pos + 1]) is not None


fpatterns = [check_shortenings, is_end, num]

IN = 0
OUT = 1

def analyze_paragraph(src_text):
    state = OUT
    splitting = []
    previous = 0
    text = src_text + " "
    """Перебираем все позиции в тексте"""
    for i in xrange(len(text)):
        if i == "\"":
            state = (state + 1) % 2
        """Если мы внутри кавычек, то не режем"""
        if state == OUT:
            for pattern in fpatterns:
                if pattern(i, text):
                    splitting += [text[previous : i + 1]]
                    previous = i + 1
                    break
    if previous == 0:
        splitting = [text]
    return splitting

def run(fr, fw):
    fw.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
    fw.write("<sentences>\n")
    for line in fr:
        stripped = line.strip()
        if stripped != "":
            print "---\nraw = ", stripped, "\n parsed = {"
            for sentence in analyze_paragraph(stripped.decode("utf-8")):
                fw.write("<sentence>" + sentence.strip().encode("utf-8") + "</sentence>\n")
                print sentence.strip()
            print "}"
    fw.write("</sentences>")

if __name__ == "__main__":
    try:
        print "in:", sys.argv[1]
        print "out:", sys.argv[2]
    except:
        print "\nPlease provide 2 arguments"
        quit()
    with open(sys.argv[2], "w+") as fw: 
        run(open(sys.argv[1], "r+"), fw)
