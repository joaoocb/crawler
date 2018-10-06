from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
import re
import json

#twitter app info	
consumer_key = 'consumer_key'
consumer_secret = 'consumer_secret'
access_token = 'access_token'
access_secret = 'access_secret'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
# api = tweepy.API(auth)

regex_str = "(?i)(eos rio|eosrio|simpleos)"

# match = re.search(r'(?i)(eos rio|eosrio|simpleos)', data["text"])

class MyListener(StreamListener):
 
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
 
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['eos'])


