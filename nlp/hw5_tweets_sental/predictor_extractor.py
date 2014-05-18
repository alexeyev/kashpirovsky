# coding:utf8

from lxml import etree
from lxml.etree import XMLParser
from StringIO import StringIO
from nltk import word_tokenize

xml = open("tweets/tweets_by_trend.xml", "r")
tree = etree.parse(xml)

current_text = u""
sent = -1

def wordset(tweet):
    return word_tokenize(tweet)

for element in tree.getroot():
    for elem in element.iter():
        if elem.tag == 'text':
            current_text = elem.text
        elif elem.tag == 'sent':
            sent = int(elem.text)
            print sent, " ".join(wordset(current_text))
            
