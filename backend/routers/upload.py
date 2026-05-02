from fastapi import APIRouter, UploadFile, File, Header, HTTPException
from database import candidates_col
from models.mongo_models import new_candidate, serialize_doc
from services.cv_parser import extract_candidate_data, parse_file_text
from services.rag_engine import rag_engine
from services.quiz_engine import quiz_engine
import os
import shutil
import uuid

router = APIRouter(prefix="/api/upload", tags=["Upload"])

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def upload_cv(
    file: UploadFile = File(...),
    user_id: str = Header(None)
):
    if not user_id:
        raise HTTPException(status_code=401, detail="user-id header zorunludur.")

    # 1. Dosyayı kaydet
    file_ext = file.filename.split(".")[-1].lower()
    if file_ext not in ["pdf", "docx", "doc"]:
        raise HTTPException(status_code=400, detail="Sadece PDF ve DOCX destekleniyor.")
    
    file_name = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print(f"LOG: Dosya kaydedildi → {file_path}")

    # 2. CV'yi analiz et (AI-free Regex tabanlı)
    candidate_data = extract_candidate_data(file_path)
    raw_text = parse_file_text(file_path)

    print(f"LOG: CV Analizi → {candidate_data.get('name')}")

    # 3. UPSERT: Mevcut profili güncelle veya yeni oluştur
    existing = candidates_col.find_one({"user_id": user_id})

    update_fields = {
        "name": candidate_data.get("name", "Bilinmeyen Aday"),
        "experience_years": candidate_data.get("experience_years", 0),
        "skills": candidate_data.get("skills", []),
        "summary": candidate_data.get("summary", ""),
        "quiz_score": 0,
        "trust_score": 0,
        "cv_indexed": False
    }

    if existing:
        print(f"LOG: Mevcut profil güncelleniyor (user_id: {user_id})")
        candidates_col.update_one({"user_id": user_id}, {"$set": update_fields})
        candidate_doc = candidates_col.find_one({"user_id": user_id})
    else:
        print(f"LOG: Yeni profil oluşturuluyor (user_id: {user_id})")
        doc = new_candidate(
            user_id=user_id,
            name=update_fields["name"],
            experience_years=update_fields["experience_years"],
            skills=update_fields["skills"],
            summary=update_fields["summary"]
        )
        result = candidates_col.insert_one(doc)
        candidate_doc = candidates_col.find_one({"_id": result.inserted_id})

    candidate_id = str(candidate_doc["_id"])

    # 4. RAG Indexleme (MongoDB Atlas Vector Search)
    try:
        rag_engine.index_cv(candidate_id, raw_text)
        candidates_col.update_one({"_id": candidate_doc["_id"]}, {"$set": {"cv_indexed": True}})
        print(f"LOG: CV Atlas'a indekslendi (candidate_id: {candidate_id})")
    except Exception as e:
        print(f"WARN: Atlas indexleme başarısız: {e}")

    # 5. Quiz üret
    quiz = await quiz_engine.generate_quiz(raw_text)

    return {
        "message": "CV başarıyla işlendi.",
        "candidate_id": candidate_id,
        "quiz": quiz
    }
