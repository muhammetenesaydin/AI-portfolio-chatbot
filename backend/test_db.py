from pymongo import MongoClient
from config import settings
from bson.objectid import ObjectId

client = MongoClient(settings.mongodb_uri)
db = client[settings.mongodb_db_name]
candidates_col = db["users"]
candidate = candidates_col.find_one({"_id": ObjectId("69f5df5ac0954e0a6b23364a")})
print("Candidate:", candidate)
