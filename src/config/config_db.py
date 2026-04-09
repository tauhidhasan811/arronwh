import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def GetDataBase():
    uri = os.environ.get("MONGO_URI")
    client = MongoClient(uri)
    db = client['arronwh']
    # print(db.list_collection_names())
    return db