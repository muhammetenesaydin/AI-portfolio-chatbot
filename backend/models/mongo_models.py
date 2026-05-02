"""
MongoDB şema yardımcıları ve veri dönüşüm fonksiyonları.
SQLAlchemy modelleri kaldırıldı, doğrudan dict tabanlı çalışıyoruz.
"""
from bson import ObjectId
from datetime import datetime

def serialize_doc(doc: dict) -> dict:
    """MongoDB dokümanını JSON-serileştirilebilir hale getirir (_id → id)."""
    if doc is None:
        return None
    doc["id"] = str(doc.pop("_id"))
    # ObjectId içeren alanları string'e çevir
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            doc[key] = str(value)
    return doc

def serialize_list(docs: list) -> list:
    """Birden fazla dokümanı serialize eder."""
    return [serialize_doc(d) for d in docs]

# ---- Şema Oluşturucular ----

def new_user(email: str, password: str, full_name: str, role: str) -> dict:
    return {
        "email": email,
        "password": password,  # TODO: üretimde bcrypt ile hashle
        "full_name": full_name,
        "role": role,  # "candidate" | "hr"
        "avatar_url": "",
        "created_at": datetime.utcnow()
    }

def new_candidate(user_id: str, name: str, experience_years: int,
                  skills: list, summary: str) -> dict:
    return {
        "user_id": user_id,
        "name": name,
        "title": "",               # Ör: "Senior Backend Developer"
        "experience_years": experience_years,
        "skills": skills,
        "summary": summary,
        "quiz_score": 0,
        "trust_score": 0,          # 0-100 arası AI Güven Skoru
        "cv_indexed": False,
        "created_at": datetime.utcnow()
    }

def new_message(sender_id: str, receiver_id: str, content: str) -> dict:
    return {
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "content": content,
        "created_at": datetime.utcnow()
    }

def new_quiz(candidate_id: str, questions: list, correct_answers: list) -> dict:
    return {
        "candidate_id": candidate_id,
        "questions": questions,
        "correct_answers": correct_answers,
        "completed": False,
        "created_at": datetime.utcnow()
    }

def calculate_trust_score(quiz_score: int, experience_years: int, skills_count: int) -> int:
    """
    AI Trust Score Hesaplama:
    - Quiz puanı: %60 ağırlık
    - Tecrübe yılı: %25 ağırlık (maks 10 yıl = 100 puan)
    - Yetenek sayısı: %15 ağırlık (maks 10 yetenek = 100 puan)
    """
    quiz_contrib = quiz_score * 0.60
    exp_contrib = min(experience_years / 10 * 100, 100) * 0.25
    skills_contrib = min(skills_count / 10 * 100, 100) * 0.15
    return int(quiz_contrib + exp_contrib + skills_contrib)
