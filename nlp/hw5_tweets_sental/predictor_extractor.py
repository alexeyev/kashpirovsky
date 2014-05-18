# coding:utf8

from lxml import etree
from lxml.etree import XMLParser
from StringIO import StringIO
from nltk import word_tokenize
import re

wordpattern = re.compile(u"[A-zА-Яа-я]+")

xml = open("tweets/tweets_by_trend.xml", "r")
tree = etree.parse(xml)

current_text = u""
sent = -1

def wordlist(tweet):
    tokenized = word_tokenize(tweet)
    filtered = [token.lower() for token in tokenized if wordpattern.match(token)]
    return filtered

for element in tree.getroot():
    for elem in element.iter():
        if elem.tag == 'text':
            current_text = elem.text
        elif elem.tag == 'sent':
            sent = int(elem.text)
            print sent, " ".join(wordlist(current_text))
            
