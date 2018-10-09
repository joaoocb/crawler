import config
#import telegram_crawler
#import twitter_crawler
#import reddit_crawler

import time

class Crawler:
    def __init__(self):
        print("__init__")

    def __del__(self):
        print("__del__")

    def start(self):
        print("start")

    def stop(self):
        print("stop")


def main():
    crawler = Crawler()
    crawler.start()

    try:
        while True:
            time.sleep(10) 
    except KeyboardInterrupt:
        print("Keyboard Interrupt received! Stoping...")
        crawler.stop()

main()
