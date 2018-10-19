import config
import sys
import json
import signal
from pyrogram import Client, Filters, MessageHandler
from pymongo import MongoClient


class TelegramCrawler():

    def __init__(self, account_name):
        signal.signal(signal.SIGINT, self.stop)
        # Setup telegram client
        self.receiver = config.TELEGRAM_CONFIG["receiver"]
        self.telegram = Client(account_name, config.TELEGRAM_CONFIG["api_id"],
                               config.TELEGRAM_CONFIG["api_hash"])
        self.telegram.add_handler(MessageHandler(self.message_handler,
                                  Filters.regex("(?i)(eos rio|eosrio|simpleos)") &
                                  Filters.text & ~Filters.private))

        # Connect to data base
        try:
            self.mongo_client = MongoClient(config.DATABASE_CONFIG["mongodb_server"],
                                            config.DATABASE_CONFIG["mongodb_port"])
            self.mongo_client.server_info()

            self.database = self.mongo_client["telegram_database"]
            self.posts = self.database["posts"]
        except:
            print("Telegram: No mongodb serve found")

    def __del__(self):
        self.mongo_client.close()
        self.telegram.stop()
        sys.exit()

    def message_handler(self, client, message):
        #print(message)
        try:
            result = self.posts.insert_one(json.loads(str(message))).inserted_id
            #print(result)
            message = "Crawler - Telegram" + "\nGroup: " + message["chat"]["title"] + "\nMessage: " + message["text"]
            self.sendmessage(message)
        except:
            print("Telegram: Error inserting data!")

    #send filtered message on telegram to spefic user
    def sendmessage(self, message):
        self.telegram.send_message(self.receiver, message)

    def run(self):
        self.telegram.start()

    def stop(self):
        self.telegram.stop()

if __name__ == '__main__':
    telegram = TelegramCrawler("my_account")
    telegram.run()
