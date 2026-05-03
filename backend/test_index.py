from pymongo import MongoClient
import requests
from config import settings
# To see index definitions, we need Atlas API or we can just try to see if $listSearchIndexes works
client = MongoClient(settings.mongodb_uri)
db = client[settings.mongodb_db_name]
col = db[settings.mongodb_collection_name]
try:
    cursor = col.aggregate([{"$listSearchIndexes": {}}])
    for doc in cursor:
        print(doc)
except Exception as e:
    print(e)
