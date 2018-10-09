import config
import re
import json
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener

#Listener handler
class MyListener(StreamListener):
    
    # Connect to data base
    def on_data(self, data):
        try:
            self.mongo_client = MongoClient(config.DATABASE_CONFIG["mongodb_server"],
                                            config.DATABASE_CONFIG["mongodb_port"])
            self.mongo_client.server_info()

            self.database = self.mongo_client["twitter_database"]
            self.posts = self.database["posts"]
        except:
            print("No mongodb serve found")
            exit()
 
    def on_error(self, status):
        print(status)
        return True

#Crawler Class
class TwitterCrawler():
    def __init__(self):
        # Setup twitter client
        self.auth = OAuthHandler(config.TWITTER_CONFIG["consumer_key"], config.TWITTER_CONFIG["consumer_secret"])
        self.auth.set_access_token(config.TWITTER_CONFIG["access_token"], config.TWITTER_CONFIG["access_secret"])
        #authenticate and create a stream
        self.twitter_stream = Stream(self.auth, MyListener())

    def run(self):
        self.twitter_stream.filter(track=['eosrio','simpleos'])

teste = TwitterCrawler()
teste.run()