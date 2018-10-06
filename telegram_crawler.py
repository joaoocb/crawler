from pyrogram import Client, Filters
from pymongo import MongoClient
import json

app = Client("my_account")

#mongodb init
try:
	client = MongoClient('localhost', 27017)
	client.server_info()
	db = client.crawler_database
	collection = db.telegram_collection
	posts = db.posts
except:
	print("No mongodb servers found")
	exit()


@app.on_message(Filters.regex("(?i)(eos rio|eosrio|simpleos)") & Filters.text & ~Filters.private)
def message_handler(client, message):
    #print("\nGroup:", message["chat"]["title"], "\nMessage:", message["text"], "\nDate:", message["date"])
    print(message)
    try:
    	result = posts.insert_one(json.loads(str(message))).inserted_id
    	print(result)
    except:
    	print("DB connection error")


app.run()