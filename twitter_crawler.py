import config
import re
import json
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener

#twitter app info   
# consumer_key = 'kkiLCRxtYmsHCcE4tmwdVinpI'
# consumer_secret = 'FRV0r23TjIvnRrYX2oPpr8wVPO1LuTe8kla2ohkIny1jMq45rP'
# access_token = '2903950480-ry3E0SPuew7gj3fX7kcA6C2FfHpdGGe1m2oMHQH'
# access_secret = 'x0uGjnL7rbuTodRfDxZd88Fe6TYyGw6NFqs0qeu2UOHMF'
 
# auth = OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_secret)

class TwitterCrawler():
    def __init__(self, StreamListener):
        # Setup twitter client
        self.twitter = OAuthHandler(config.TWITTER_CONFIG["consumer_key"], config.TWITTER_CONFIG["consumer_secret"])
        self.auth.set_access_token(config.TWITTER_CONFIG["access_token"], config.TWITTER_CONFIG["access_secret"])
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

    def run(self):
        twitter_stream = Stream(auth, TwitterCrawler())
        twitter_stream.filter(track=['eosrio','simpleos'])
