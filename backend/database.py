"""
MongoDB Atlas bağlantı modülü.
SQLite/SQLAlchemy tamamen kaldırıldı, tüm veriler tek MongoDB Atlas'ta toplanıyor.
"""
from pymongo import MongoClient, ASCENDING
from pymongo.collection import Collection
from config import settings
import os

# MongoDB Bağlantısı
client = MongoClient(settings.mongodb_uri)
mongo_db = client[settings.mongodb_db_name]

# Koleksiyonlar
users_col: Collection = mongo_db["users"]
candidates_col: Collection = mongo_db["candidates"]
messages_col: Collection = mongo_db["messages"]
quizzes_col: Collection = mongo_db["quizzes"]
cv_vectors_col: Collection = mongo_db["cv_vectors"]

# İndeksler (ilk çalıştırmada oluşturulur)
def create_indexes():
    try:
        users_col.create_index([("email", ASCENDING)], unique=True)
        candidates_col.create_index([("user_id", ASCENDING)])
        messages_col.create_index([("sender_id", ASCENDING), ("receiver_id", ASCENDING)])
        print("LOG: MongoDB indeksleri hazır.")
    except Exception as e:
        print(f"LOG: İndeks oluşturma (zaten mevcut olabilir): {e}")

create_indexes()

def get_db():
    """FastAPI Dependency — MongoDB veritabanı nesnesi döner."""
    return mongo_db
