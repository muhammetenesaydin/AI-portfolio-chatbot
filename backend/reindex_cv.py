"""
CV Geçiş Script'i (RAG -> Full Context)
-------------------------------
Eski vektör veritabanını temizler ve mevcut CV'lerin metinlerini 
doğrudan 'candidates' (users) koleksiyonuna cv_text olarak ekler.

Kullanım:
    python3 reindex_cv.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from pymongo import MongoClient
from config import settings
from services.cv_parser import parse_file_text

def migrate_to_full_context():
    client = MongoClient(settings.mongodb_uri)
    db = client[settings.mongodb_db_name]

    # 1. Eski vektör koleksiyonunu temizle (Artık kullanılmıyor)
    vector_col = db[settings.mongodb_collection_name]
    count_before = vector_col.count_documents({})
    print(f"🗑️  Gereksiz vektörler siliniyor... ({count_before} kayıt)")
    vector_col.delete_many({})
    print("✅ Vektör koleksiyonu temizlendi.")

    # 2. Adaylar koleksiyonundan CV yollarını al
    users_col = db["users"] # Aslında upload'ta candidates_col diye geçiyor ancak mongo'daki adı "users" olabilir mi?
    # Kontrol edelim. upload.py candidates_col olarak kaydediyor (database.py'de candidates_col = mongo_db["candidates"])
    # Fakat quiz_score vs "users" a da eklenmiş olabilir. database.py'de users ve candidates ayrı. 
    candidates_col = db["candidates"]
    
    candidates = list(candidates_col.find({"cv_text": {"$exists": False}}))
    
    # Ayrıca 'users' tablosunda role=candidate olanlar varsa onları da alalım
    users_with_cv = list(users_col.find({"role": "candidate", "cv_path": {"$exists": True}}))
    
    candidates_to_process = candidates + users_with_cv

    if not candidates_to_process:
        print("\n⚠️  Güncellenecek aday bulunamadı.")
        return

    # 3. Her aday için CV metnini db'ye kaydet
    success, failed = 0, 0
    for candidate in candidates_to_process:
        user_id = str(candidate["_id"])
        cv_path = candidate.get("cv_path")
        name = candidate.get("name", candidate.get("full_name", "Bilinmeyen"))

        if not cv_path or not os.path.exists(cv_path):
            # Yükleme klasöründen bulmayı deneyelim.
            # Fakat cv_path yoksa geç.
            continue

        print(f"\n📄 [{name}] cv_text ekleniyor... (ID: {user_id})")
        try:
            text = parse_file_text(cv_path)
            if not text.strip():
                print(f"   ⚠️  CV metni boş, atlanıyor.")
                failed += 1
                continue

            # Koleksiyonu bul (users'tan geldiyse users'ı, candidates'ten geldiyse candidates'i güncelle)
            if "role" in candidate:
                users_col.update_one({"_id": candidate["_id"]}, {"$set": {"cv_text": text}})
            else:
                candidates_col.update_one({"_id": candidate["_id"]}, {"$set": {"cv_text": text}})
                
            print(f"   ✅ Başarıyla cv_text veritabanına işlendi.")
            success += 1
        except Exception as e:
            print(f"   ❌ Hata: {e}")
            failed += 1

    print(f"\n🎉 Geçiş Tamamlandı! ✅ {success} başarılı / ❌ {failed} başarısız")

if __name__ == "__main__":
    migrate_to_full_context()
