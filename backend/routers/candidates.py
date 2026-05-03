from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import candidates_col, users_col
from models.mongo_models import serialize_doc, serialize_list, calculate_trust_score
from bson import ObjectId

router = APIRouter(prefix="/api/candidates", tags=["Candidates"])

@router.get("/")
def get_candidates():
    """Tüm adayları listeler (İK paneli için)."""
    candidates = list(candidates_col.find())
    return serialize_list(candidates)

@router.get("/my-profile/{user_id}")
def get_my_profile(user_id: str):
    """Adayın kendi profilini getirir."""
    candidate = candidates_col.find_one({"user_id": user_id})
    if not candidate:
        return None
    return serialize_doc(candidate)

@router.get("/my-quizzes/{user_id}")
def get_my_quizzes(user_id: str):
    """Kullanıcının geçmiş sınavlarını listeler."""
    results = list(candidates_col.find({"user_id": user_id}))
    return serialize_list(results)

@router.get("/{candidate_id}")
def get_candidate(candidate_id: str):
    """Tekil aday profilini getirir."""
    try:
        candidate = candidates_col.find_one({"_id": ObjectId(candidate_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Geçersiz ID formatı.")
    if not candidate:
        raise HTTPException(status_code=404, detail="Aday bulunamadı.")
    return serialize_doc(candidate)

class QuizSubmit(BaseModel):
    candidate_id: str
    answers: list

@router.post("/{candidate_id}/quiz/submit")
def submit_quiz(candidate_id: str, req: QuizSubmit):
    """Quiz cevaplarını değerlendirir ve Trust Score'u günceller."""
    try:
        candidate = candidates_col.find_one({"_id": ObjectId(candidate_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Geçersiz ID.")
    if not candidate:
        raise HTTPException(status_code=404, detail="Aday bulunamadı.")

    # Doğru cevapları db'den çek
    correct_answers = candidate.get("quiz_correct_answers", [])
    
    if not correct_answers:
        # Eğer bir nedenden ötürü db'de doğru cevaplar yoksa (eski veri vs.) varsayılan hesaplama yapma
        quiz_score = 0
    else:
        # Puan hesapla (Doğru eşleşen cevaplar / Toplam soru * 100)
        correct_count = sum(
            1 for idx, user_ans in enumerate(req.answers) 
            if idx < len(correct_answers) and user_ans == correct_answers[idx]
        )
        total_questions = len(correct_answers)
        quiz_score = int((correct_count / total_questions) * 100) if total_questions > 0 else 0

    # Trust Score hesapla
    trust_score = calculate_trust_score(
        quiz_score=quiz_score,
        experience_years=candidate.get("experience_years", 0),
        skills_count=len(candidate.get("skills", []))
    )

    candidates_col.update_one(
        {"_id": ObjectId(candidate_id)},
        {"$set": {"quiz_score": quiz_score, "trust_score": trust_score}}
    )
    return {"quiz_score": quiz_score, "trust_score": trust_score}
