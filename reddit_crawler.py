#! usr/bin/env python3
import praw
import re

CLIENT_ID = 'lbUv4p2Fa11vyw'
CLIENT_SECRET = 'S1MeJIXIt47AglQv_HsPsYlS0g8'
USER_AGENT = 'reddit_crawler'
USERNAME = ''
PASSWORD = ''

topics = {"title":[],
          "score":[],
          "id":[], "url":[],
          "comms_num": [],
          "created": [],
          "body":[]}

def run():
    reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT,
                     username=USERNAME, password=PASSWORD)

    readSubreddit(reddit.subreddit('eos'));

def readSubreddit(subreddit):
    for submission in subreddit.stream.submissions():
        if(re.search(r'eos rio|eosrio|simpleos', submission.title, re.IGNORECASE)):
            topics["title"].append(submission.title)
            topics["score"].append(submission.score)
            topics["id"].append(submission.id)
            topics["url"].append(submission.url)
            topics["comms_num"].append(submission.num_comments)
            topics["created"].append(submission.created)
            topics["body"].append(submission.selftext)

            print(submission.title)
            #saveTopic()

#def saveTopic():
    #save new topic to DB

run()
