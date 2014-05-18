# coding:utf8

from lxml import etree
from lxml.etree import XMLParser
from StringIO import StringIO
from nltk import word_tokenize
import re
from nltk.stem.snowball import RussianStemmer
import math

wordpattern = re.compile(u"[A-zА-Яа-я]+")

current_text = u""
sent = -1

def wordlist(tweet):
    tokenized = word_tokenize(tweet)
    #filtered = [RussianStemmer().stem(token.lower()) for token in tokenized if wordpattern.match(token)]
    filtered = [token.lower() for token in tokenized if wordpattern.match(token)]
    return filtered

def get_stats():
    xml = open("tweets/learn.xml", "r")
    tree = etree.parse(xml)
    stats = dict()
    words = set()
    for element in tree.getroot():
        for elem in element.iter():
            if elem.tag == 'text':
                current_text = elem.text
            elif elem.tag == 'sent':
                sent = int(elem.text)
                for word in wordlist(current_text):
                    if not (sent, word) in stats:
                        stats[(sent, word)] = 0
                    if not ((sent + 1) % 2, word) in stats:
                        stats[((sent + 1) % 2, word)] = 0
                    stats[(sent, word)] += 1
                    words.add(word)
    return stats, words

def get_top(k):
    stats, words = get_stats()
    #for k, v in stats:
    #    print stats[(k,v)], k, v
    """ PMI
    p(xy)       c(1, w) * total     c(1, w)
    -------- = ----------------- ~ ---------
    p(x)p(y)    c(1) * c(w)         c(w)
    """
    return sorted([(-( (stats[(1, w)] - stats[(0, w)] + 1) * math.log(1 + stats[(1, w)]) / (1 + math.log(stats[(1, w)] + stats[(0, w)]))), w) for w in words])[:200]

for k,v in get_top(100):
    print -k, v

