#! usr/bin/env python3
import praw
from pymongo import MongoClient
import re

#TODO: This information shlud be in a config file
CLIENT_ID = "lbUv4p2Fa11vyw"
CLIENT_SECRET = "S1MeJIXIt47AglQv_HsPsYlS0g8"
USER_AGENT = "reddit_crawler"
USERNAME = "joaoocb"
PASSWORD = "vrat$8#9"
MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017

class RedditCrawler:

    def __init__(self, subreddit_name):
        # Create reddit and subreddit instances
        self.reddit = praw.Reddit(client_id = CLIENT_ID, client_secret = CLIENT_SECRET,
                                  user_agent = USER_AGENT, username = USERNAME,
                                  password = PASSWORD)
        self.subreddit = self.reddit.subreddit(subreddit_name)

        # Connect to data base
        try:
            self.mongo_client = MongoClient(MONGODB_SERVER, MONGODB_PORT)
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

                self.colection.insert_one(topic)

    def run(self):
        self.readTopics()

reddit = RedditCrawler("eos")
reddit.run()
