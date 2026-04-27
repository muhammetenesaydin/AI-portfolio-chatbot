from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_, distinct
from database import get_db
from models.db_models import Message, User
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/api/messages", tags=["Messages"])

class MessageSend(BaseModel):
    sender_id: int
    receiver_id: int
    content: str

@router.get("/history/{user_id}/{other_id}")
def get_history(user_id: int, other_id: int, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(
        or_(
            and_(Message.sender_id == user_id, Message.receiver_id == other_id),
            and_(Message.sender_id == other_id, Message.receiver_id == user_id)
        )
    ).order_by(Message.id.asc()).all()
    return messages

@router.post("/send")
def send_message(msg: MessageSend, db: Session = Depends(get_db)):
    new_msg = Message(
        sender_id=msg.sender_id,
        receiver_id=msg.receiver_id,
        content=msg.content,
        created_at=datetime.now().strftime("%H:%M")
    )
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    return new_msg

@router.get("/active-chats/{user_id}")
def get_active_chats(user_id: int, db: Session = Depends(get_db)):
    # Kullanıcının mesajlaştığı benzersiz kişilerin ID'lerini bul
    sent_to = db.query(Message.receiver_id).filter(Message.sender_id == user_id)
    received_from = db.query(Message.sender_id).filter(Message.receiver_id == user_id)
    
    partner_ids = sent_to.union(received_from).all()
    ids = [p[0] for p in partner_ids if p[0] != user_id]
    
    # Bu ID'lere sahip kullanıcı bilgilerini getir
    users = db.query(User).filter(User.id.in_(ids)).all()
    return users

from sqlalchemy import and_ # Eksik import eklendi
