import config
import re
import json
import sys
from pymongo import MongoClient
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
from pyrogram import Client

#Listener handler
class MyListener(StreamListener):
    def __init__(self):

        #Setup telegram client
        self.receiver = config.TELEGRAM_CONFIG["receiver"]
        self.telegram = Client(config.TELEGRAM_CONFIG["account_name"], config.TELEGRAM_CONFIG["api_id"],
                               config.TELEGRAM_CONFIG["api_hash"])
        self.telegram.start()
        
        # Connect to data base
        try:
            self.mongo_client = MongoClient(config.DATABASE_CONFIG["mongodb_server"],
                                            config.DATABASE_CONFIG["mongodb_port"])
            self.mongo_client.server_info()
            self.database = self.mongo_client["twitter_database"]
            self.posts = self.database["posts"]
        except:
            print("Twitter: No mongodb serve found")
            sys.exit()

    def on_data(self, data):
        try:
            result = self.posts.insert_one(json.loads(str(data))).inserted_id
            #print(result)
            self.sendmessage(json.loads(data))
            return True

        except:
            print("Twitter: Error inserting data!")

    #send filtered message on telegram to spefic user
    def sendmessage(self, message):
        message = "Crawler - Twitter" + "\nUser: " + message["user"]["screen_name"] + "\nTweet: " + message["text"]
        #print(message)
        self.telegram.send_message(self.receiver, message)
 
    def on_error(self, status):
        print(status)
        return True

    def __del__(self):
        self.mongo_client.close()
        self.telegram.stop()

#Crawler Class
class TwitterCrawler():
    def __init__(self):
        # Setup twitter client
        self.auth = OAuthHandler(config.TWITTER_CONFIG["consumer_key"], config.TWITTER_CONFIG["consumer_secret"])
        self.auth.set_access_token(config.TWITTER_CONFIG["access_token"], config.TWITTER_CONFIG["access_secret"])
        #authenticate and create a stream
        self.my_listener = MyListener()
        self.twitter_stream = Stream(self.auth, MyListener())

    def run(self):
        self.twitter_stream.filter(track=['eosrio','simpleos'])

    def __del__(self):
        self.twitter_stream.disconnect()

if __name__ == '__main__':
    twitter = TwitterCrawler()
    twitter.run()