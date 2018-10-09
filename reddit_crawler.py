import config
import threading
from praw import Reddit
from pymongo import MongoClient
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

        # Connect to data base
        try:
            self.mongo_client = MongoClient(config.DATABASE_CONFIG["mongodb_server"],
                                            config.DATABASE_CONFIG["mongodb_port"])
            self.mongo_client.server_info()

            self.database = self.mongo_client["reddit_database"]
            self.colection = self.database["topics"]
        except:
            print("No mongodb serve found")
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
                        print(result)
                    except:
                        print("Failed to insert data to DataBase")

            #TODO: Check for new comments

            # Check if thread should end
            self.threadLock.acquire()
            if self.stop:
                break
            self.threadLock.release()

    def run(self):
        self.readTopics()

    def stop(self):
        self.threadLock.acquire()
        self.stop = True
        self.threadLock.release()

reddit = RedditCrawler("eos")
reddit.run()
