import config
import threading
from praw import Reddit
from pymongo import MongoClient
from pyrogram import Client
import re

class RedditCrawler(threading.Thread):

    def __init__(self, subreddit_name):
        threading.Thread.__init__(self)
        self.threadLock = threading.Lock()
        self.stop = False

        # Create reddit and subreddit instances
        self.reddit = Reddit(client_id =     config.REDDIT_CONFIG["client_id"],
                             client_secret = config.REDDIT_CONFIG["client_secret"],
                             user_agent =    config.REDDIT_CONFIG["user_agent"],
                             username =      config.REDDIT_CONFIG["username"],
                             password =      config.REDDIT_CONFIG["password"])
        self.subreddit = self.reddit.subreddit(subreddit_name)

        # # Setup telegram client
        # self.receiver = config.TELEGRAM_CONFIG["receiver"]
        # self.telegram = Client(config.TELEGRAM_CONFIG["account_name"], config.TELEGRAM_CONFIG["api_id"],
        #                        config.TELEGRAM_CONFIG["api_hash"])
        # self.telegram.start()

        # Connect to data base
        try:
            self.mongo_client = MongoClient(config.DATABASE_CONFIG["mongodb_server"],
                                            config.DATABASE_CONFIG["mongodb_port"])
            self.mongo_client.server_info()

            self.database = self.mongo_client["reddit_database"]
            self.colection = self.database["topics"]
        except:
            print("Reddit: No mongodb serve found")
            exit()

    def __del__(self):
        self.mongo_client.close()

    def readTopics(self):
        while True:
            # Check for now topics
            for submission in self.subreddit.stream.submissions(pause_after = 0):
                if submission is None:
                    break
                elif(re.search(r"eos rio|eosrio|simpleos", submission.title, re.IGNORECASE)):
                    topic = {"title":        submission.title,
                             "score":        submission.score,
                             "id":           submission.id,
                             "url":          submission.url,
                             "num_comments": submission.num_comments,
                             "created":      submission.created,
                             "body":         submission.selftext}

                    try:
                        result = self.colection.insert_one(topic).inserted_id
                        #self.sendmessage(topic)
                        #print(result)
                    except:
                        print("Reedit: Error inserting data!")

            #TODO: Check for new comments

            # Check if thread should end
            self.threadLock.acquire()
            if self.stop:
                break
            self.threadLock.release()

    #send filtered message on telegram to spefic user
    def sendmessage(self, message):
        message = "Crawler - Reddit" + "\nTitle: " + message["title"] + "\nMessage: " + message["body"] + "\nUrl: " + message["url"]
        #self.telegram.send_message(self.receiver, message)

    def run(self):
        self.readTopics()

    def stop(self):
        self.threadLock.acquire()
        self.stop = True
        self.threadLock.release()
        #self.telegram.stop()

if __name__ == '__main__':
    reddit = RedditCrawler("eos")
    reddit.run()
