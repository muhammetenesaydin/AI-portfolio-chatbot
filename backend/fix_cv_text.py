import sys
import os
from pymongo import MongoClient
from config import settings
from services.cv_parser import parse_file_text
from bson.objectid import ObjectId

client = MongoClient(settings.mongodb_uri)
db = client[settings.mongodb_db_name]

text = parse_file_text("data/uploads/6f96a379-1bc7-4a4e-89da-437d5449606f.pdf")
res = db["candidates"].update_one(
    {"_id": ObjectId("69f5df5ac0954e0a6b23364a")},
    {"$set": {"cv_text": text}}
)
print("Updated:", res.modified_count)
