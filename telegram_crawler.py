import config
from pyrogram import Client, Filters, MessageHandler
from pymongo import MongoClient
import json

class TelegramCrawler:

    def __init__(self, account_name):
        # Setup telegram client
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
            print("No mongodb serve found")
            exit()

    def message_handler(self, client, message):
        #print("\nGroup:", message["chat"]["title"], "\nMessage:", message["text"],
        #"\nDate:", message["date"])
        print(message)

        try:
        	result = self.posts.insert_one(json.loads(str(message))).inserted_id
        	print(result)
        except:
            print("Failed to insert data to DataBase")

    def run(self):
        self.telegram.run()

telegram = TelegramCrawler("my_account")
telegram.run()
