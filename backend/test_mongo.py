from pymongo import MongoClient
from config import settings
client = MongoClient(settings.mongodb_uri)
db = client[settings.mongodb_db_name]
col = db[settings.mongodb_collection_name]
print("Total docs:", col.count_documents({}))
doc = col.find_one({})
if doc:
    print("Doc keys:", doc.keys())
    print("Candidate ID:", doc.get("candidate_id"))
    emb = doc.get("embedding")
    print("Embedding size:", len(emb) if emb else "None")
else:
    print("No docs!")
