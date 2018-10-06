#! usr/bin/env python3
import config
from praw import Reddit
from pymongo import MongoClient
import re

class RedditCrawler:

    def __init__(self, subreddit_name):
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

    def readTopics(self):
        for submission in self.subreddit.stream.submissions():
            if(re.search(r"eos rio|eosrio|simpleos", submission.title, re.IGNORECASE)):
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

    def run(self):
        self.readTopics()

reddit = RedditCrawler("eos")
reddit.run()
