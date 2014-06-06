# -*- coding: utf-8 -*-
import ConfigParser
from TwitterAPI import TwitterAPI
from lxml import etree
#from examples.streaming import StdOutListener
from lxml.etree import XMLParser
from tweepy import StreamListener, OAuthHandler, Stream, API, Cursor
import tweepy

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
        self.save(self.positive_tweets, "tweets/positive.xml", 1)

        self.grab_tweets(self.negative_query, self.negative_tweets)
        self.save(self.negative_tweets, "tweets/negative.xml", 0)

    def save(self, tweets, file_name, parameter):
        root = etree.Element('tweets')
        for tweet in tweets:
            child = etree.Element('tweet')            
            text_child = etree.Element('text')
            text_child.text = tweet
            sent_child = etree.Element('sent')
            sent_child.text = str(parameter)
            child.append(text_child)
            child.append(sent_child)
            root.append(child)
        f = open(file_name, "w+")
        f.write(etree.tostring(root, pretty_print=True, encoding='UTF-8'))
        f.close()

    def save_for_markup(self, tweets, file_name):
        root = etree.Element('tweets')
        for tweet in tweets:
            child = etree.Element('tweet')
            text_child = etree.Element('text')
            text_child.text = tweet
            sent_child = etree.Element('sent')
            sent_child.text = ""
            child.append(text_child)
            child.append(sent_child)
            root.append(child)
        f = open(file_name, "w+")
        f.write(etree.tostring(root, pretty_print=True, encoding='UTF-8'))
        f.close()


    # read example
    def read(self):
        xml = open("tweets/positive.xml", "r").read().decode("utf-8")
        doc = etree.fromstring(xml)
        for child in doc:
            print child.text

    def download_tweets_by_trend(self):
        tweets_count = 200
        counter = 0
        tweets = set()
        for tweet in Cursor(self.api.search,
                            q="#питер", count=1000000,
                            lang="ru").items():
            print "tweet found: ", tweet.text
            if len(tweet.text) > 30:
                tweets.add(tweet.text)
                counter += 1
            if counter > tweets_count:
                break
        self.save(tweets, "tweets/tweets_by_trend.xml")

    def download_tweets_by_trend_2(self):
        api = TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)
        tweets = set()
        limit = 2000
        counter = 0
        dates = ['2014-05-18', '2014-05-17', '2014-05-16', '2014-05-15', '2014-05-14', '2014-05-13','2014-05-12','2014-05-11','2014-05-10','2014-05-09','2014-05-08','2014-05-07', '2014-05-06', '2014-05-03', '2014-05-05', '2014-05-04', '2014-05-02', '2014-05-01', '2014-04-07', '2014-04-20','2014-05-19','2014-04-05']
        for date in dates:
            r = api.request('search/tweets', {'q': ':) OR =) OR ;)', 'lang': 'ru', 'count': '10000', 'until': date})
            for item in r.get_iterator():
                if len(item['text']) > 30:
                    tweets.add(item['text'])
                    counter += 1
                if counter >= limit:
                    break
            if counter >= limit:
                break

        self.save_for_markup(tweets, "tweets/tweets_smile_neg.xml")


downloader = TweetsDownloader()
downloader.download()
# downloader.read()
#downloader.download_tweets_by_trend_2()
