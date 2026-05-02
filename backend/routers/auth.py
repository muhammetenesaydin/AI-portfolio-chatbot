from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from database import get_db, users_col
from models.mongo_models import new_user, serialize_doc
from datetime import datetime

router = APIRouter(prefix="/api/auth", tags=["Auth"])

class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: str
    role: str = "candidate"

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(req: RegisterRequest):
    if users_col.find_one({"email": req.email}):
        raise HTTPException(status_code=400, detail="Bu e-posta zaten kayıtlı.")
    
    user_doc = new_user(req.email, req.password, req.full_name, req.role)
    result = users_col.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id
    return serialize_doc(user_doc)

@router.post("/login")
def login(req: LoginRequest):
    user = users_col.find_one({"email": req.email, "password": req.password})
    if not user:
        raise HTTPException(status_code=401, detail="E-posta veya şifre hatalı.")
    return serialize_doc(user)
