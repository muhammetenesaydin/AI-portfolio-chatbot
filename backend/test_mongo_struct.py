from pymongo import MongoClient
from config import settings
import json
client = MongoClient(settings.mongodb_uri)
db = client[settings.mongodb_db_name]
col = db[settings.mongodb_collection_name]
doc = col.find_one()
if doc:
    doc.pop("embedding", None)
    doc["_id"] = str(doc["_id"])
    print(json.dumps(doc, indent=2))
