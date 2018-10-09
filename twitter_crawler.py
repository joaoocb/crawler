import config
import re
import json
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener

#Listener handler
class MyListener(StreamListener):
    
    #TODO save to mongodb
    def on_data(self, data):
        try:
            with open('python.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True

#Crawler Class
class TwitterCrawler():
    def __init__(self):
        # Setup twitter client
        self.auth = OAuthHandler(config.TWITTER_CONFIG["consumer_key"], config.TWITTER_CONFIG["consumer_secret"])
        self.auth.set_access_token(config.TWITTER_CONFIG["access_token"], config.TWITTER_CONFIG["access_secret"])

    def run(self):
        twitter_stream = Stream(self.auth, MyListener())
        twitter_stream.filter(track=['eosrio','simpleos'])

teste = TwitterCrawler()
teste.run()