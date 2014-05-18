# -*- coding: utf-8 -*-
import ConfigParser
from lxml import etree
from examples.streaming import StdOutListener
from lxml.etree import XMLParser
from tweepy import StreamListener, OAuthHandler, Stream, API, Cursor

__author__ = 'achugr'

config = ConfigParser.RawConfigParser()
config.read('api_key.cfg')

consumer_key = config.get("section1", "consumer_key")
consumer_secret = config.get("section1", "consumer_secret")
access_token = config.get("section1", "access_token")
access_token_secret = config.get("section1", "access_token_secret")


class TweetsDownloader:
    def __init__(self):
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = API(auth)
        self.tweets_count = 2000
        self.positive_query = ":) OR :D OR ;) OR =)"
        self.negative_query = ":( OR =( OR ;-("
        self.positive_tweets = set()
        self.negative_tweets = set()


    def grab_tweets(self, query, tweets):
        ok_tweets_count = 0
        for tweet in Cursor(self.api.search,
                            q=query,
                            count=100,
                            include_entities=True,
                            lang="ru").items():
            if len(tweet.text) > 30:
                tweets.add(tweet.text)
                print "tweets set size: ", len(tweets)
                print tweet.text
                ok_tweets_count += 1
            if ok_tweets_count > self.tweets_count:
                break


    def download(self):
        self.grab_tweets(self.positive_query, self.positive_tweets)
        self.save(self.positive_tweets, "tweets/positive.xml")

        self.grab_tweets(self.negative_query, self.negative_tweets)
        self.save(self.negative_tweets, "tweets/negative.xml")

    def save(self, tweets, file_name):
        root = etree.Element('tweets')
        for tweet in tweets:
            child = etree.Element('tweet')
            child.text = tweet
            root.append(child)
        f = open(file_name, "w")
        f.write(etree.tostring(root, pretty_print=True, encoding='UTF-8'))
        f.close()


    # read example
    def read(self):
        xml = open("tweets/positive.xml", "r").read().decode("utf-8")
        doc = etree.fromstring(xml)
        for child in doc:
            print child.text


downloader = TweetsDownloader()
downloader.download()
# downloader.read()
