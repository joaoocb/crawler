import config
import threading
from pyrogram import Client, Filters, MessageHandler
from pymongo import MongoClient
import json

class TelegramCrawler(threading.Thread):

    def __init__(self, account_name):
        threading.Thread.__init__(self)

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
            exit()

    def __del__(self):
        self.mongo_client.close()

    def message_handler(self, client, message):
        #print(message)
        try:
            result = self.posts.insert_one(json.loads(str(message))).inserted_id
            #print(result)
            self.sendmessage(message)
        except:
            print("Telegram: Error inserting data!")

    #send filtered message on telegram to spefic user
    def sendmessage(self, message):
        message = "Crawler - Telegram" + "\nGroup: " + message["chat"]["title"] + "\nMessage: " + message["text"]
        self.telegram.send_message(self.receiver, message)

    def run(self):
        self.telegram.run()

    def stop(self):
        self.telegram.stop()

telegram = TelegramCrawler("my_account")
telegram.run()
