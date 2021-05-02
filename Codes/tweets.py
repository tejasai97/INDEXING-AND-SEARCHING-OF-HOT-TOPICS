import json
from kafka import SimpleProducer, KafkaClient
import tweepy
import configparser
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from nltk.stem import PorterStemmer
import re
from probables import (BloomFilter)
from probables import (HeavyHitters)
from textblob import TextBlob


#To stream twitter data
class TweeterStreamListener(tweepy.StreamListener):
    

    def __init__(self, api):
        self.api = api
        super(tweepy.StreamListener, self).__init__()
        client = KafkaClient("localhost:9092")

        self.producer = SimpleProducer(client, async = True,
                          batch_send_every_n = 1000,
                          batch_send_every_t = 10)
        
        #Initializing bloom filter 
        global punc
        punc = '''!()-[]{};:"\,<>./?@#$%^&*_~'''
        
        global blm
        blm = BloomFilter(est_elements=150, false_positive_rate=0.05)
        
        stop_words = [u'a', u'about', u'above', u'after', u'again', u'against', u'all', u'am', u'an', u'and', u'any', u'are', u"aren't", u'as', u'at', u'be', u'because', u'been', u'before', u'being', u'below', u'between', u'both', u'but', u'by', u"can't", u'cannot', u'could', u"couldn't", u'did', u"didn't", u'do', u'does', u"doesn't", u'doing', u"don't", u'down', u'during', u'each', u'few', u'for', u'from', u'further', u'had', u"hadn't", u'has', u"hasn't", u'have', u"haven't", u'having', u'he', u"he'd", u"he'll", u"he's", u'her', u'here', u"here's", u'hers', u'herself', u'him', u'himself', u'his', u'how', u"how's", u'i', u"i'd", u"i'll", u"i'm", u"i've", u'if', u'in', u'into', u'is', u"isn't", u'it', u"it's", u'its', u'itself', u"let's", u'me', u'more', u'most', u"mustn't", u'my', u'myself', u'no', u'nor', u'not', u'of', u'off', u'on', u'once', u'only', u'or', u'other', u'ought', u'our', u'ours', u'ourselves', u'out', u'over', u'own', u'same', u"shan't", u'she', u"she'd", u"she'll", u"she's", u'should', u"shouldn't", u'so', u'some', u'such', u'than', u'that', u"that's", u'the', u'their', u'theirs', u'them', u'themselves', u'then', u'there', u"there's", u'these', u'they', u"they'd", u"they'll", u"they're", u"they've", u'this', u'those', u'through', u'to', u'too', u'under', u'until', u'up', u'very', u'was', u"wasn't", u'we', u"we'd", u"we'll", u"we're", u"we've", u'were', u"weren't", u'what', u"what's", u'when', u"when's", u'where', u"where's", u'which', u'while', u'who', u"who's", u'whom', u'why', u"why's", u'with', u"won't", u'would', u"wouldn't", u'you', u"you'd", u"you'll", u"you're", u"you've", u'your', u'yours', u'yourself', u'yourselves',u' ',u't',u'm',u'http',u'https',u'amp',u"nt",u"https",u"get",u"got",u'will',u'can',u'don']
        
        for item in stop_words:
                blm.add(item)
        

    def on_status(self, status):
        
        #Pre processing tweets data before pushing it to kafka
        
        msg = {}
        word_list = word_tokenize(status.text)
        words = []
        for word in word_list:
            if((blm.check(word.lower()) == False and blm.check(word)==False)):
                for x in word.lower(): 
                    if x in punc: 
                        word = word.replace(x, "") 
                if (len(word)>2):
                    words.append(word)
        
        msg['tokenized'] = words
        msg['text'] = status.text
        
        tweet = TextBlob(status.text)

        # determine if sentiment is positive, negative, or neutral
        
        if tweet.sentiment.polarity < 0:
            sentiment = "negative"
        elif tweet.sentiment.polarity == 0:
            sentiment = "neutral"
        else:
            sentiment = "positive"

       
        msg['sentiment'] = sentiment
        try:
	    data = json.dumps(msg)
            self.producer.send_messages(b'twitterPost', data)
            #Kafka push complete!
        except Exception as e:
            print(e)
            return False
        return True

    def on_error(self, status_code):
        print("Error received in kafka producer")
        return True # Don't kill the stream

    def on_timeout(self):
        return True # Don't kill the stream

if __name__ == '__main__':

    # Read the credententials from 'twitter.txt' file
    config = configparser.ConfigParser()
    config.read('twitter.txt')
    consumer_key = config['DEFAULT']['consumerKey']
    consumer_secret = config['DEFAULT']['consumerSecret']
    access_key = config['DEFAULT']['accessToken']
    access_secret = config['DEFAULT']['accessTokenSecret']

    # Create Auth object
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    stream = tweepy.Stream(auth, listener = TweeterStreamListener(api))

    #We can change location accordingly or even add topics to stream
    stream.filter(locations=[-180,-90,180,90], languages = ['en'])

