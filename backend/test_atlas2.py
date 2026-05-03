import sys
from pymongo import MongoClient
from config import settings

client = MongoClient(settings.mongodb_uri)
db = client[settings.mongodb_db_name]
col = db[settings.mongodb_collection_name]

print("Checking index...")
try:
    for doc in col.aggregate([{"$listSearchIndexes": {}}]):
        print(doc)
except Exception as e:
    print("Error listing indexes:", e)

print("Checking vector search error...")
try:
    results = col.aggregate([
        {
            "$vectorSearch": {
                "index": settings.mongodb_index_name,
                "path": "embedding",
                "queryVector": [0.0]*768,
                "numCandidates": 10,
                "limit": 3
            }
        }
    ])
    docs = list(results)
    print("Zero vector query docs found:", len(docs))
except Exception as e:
    print("Error in vectorSearch:", e)
