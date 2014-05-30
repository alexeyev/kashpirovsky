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
    xml = open("tweets/negative.xml", "r")
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


def get_stats(file_name, stats, words):
    sent = 0
    if file_name.__contains__("positive"):
        sent = 1
    xml = open("tweets/" + file_name, "r")
    tree = etree.parse(xml)
    for element in tree.getroot().findall("tweet"):
        current_text = element.text
        for word in wordlist(current_text):
            if not (sent, word) in stats:
                stats[(sent, word)] = 0
            if not ((sent + 1) % 2, word) in stats:
                stats[((sent + 1) % 2, word)] = 0
            stats[(sent, word)] += 1
            words.add(word)


def get_top(k, stats, words, clazz):
    #for k, v in stats:
    #    print stats[(k,v)], k, v
    """ PMI
    p(xy)       c(1, w) * total     c(1, w)
    -------- = ----------------- ~ ---------
    p(x)p(y)    c(1) * c(w)         c(w)
    """
    other_clazz = (clazz + 1) % 2
    return sorted([(-(
        (stats[(clazz, w)] - stats[(other_clazz, w)] + 1) * math.log(1 + stats[(clazz, w)]) / (
            1 + math.log(stats[(clazz, w)] + stats[(other_clazz, w)]))),
                    w) for w in words])[:k]


def save(file_name, results):
    f = open("tweets/" + file_name, "w")
    for k, v in results:
        print "v is: " + v
        f.write(v.encode("utf-8"))
        f.write("\n")
    f.close()


stats = dict()
words = set()
get_stats("positive.xml", stats, words)
get_stats("negative.xml", stats, words)

save("negative_keywords_filtered.txt", get_top(200, stats, words, 0))
save("positive_keywords_filtered.txt", get_top(200, stats, words, 1))
