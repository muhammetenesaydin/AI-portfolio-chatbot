from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import messages_col, users_col
from models.mongo_models import new_message, serialize_doc, serialize_list
from bson import ObjectId

router = APIRouter(prefix="/api/messages", tags=["Messages"])

class MessageSend(BaseModel):
    sender_id: str
    receiver_id: str
    content: str

@router.post("/send")
def send_message(msg: MessageSend):
    """Mesaj gönderir ve veritabanına kaydeder."""
    doc = new_message(msg.sender_id, msg.receiver_id, msg.content)
    result = messages_col.insert_one(doc)
    doc["_id"] = result.inserted_id
    return serialize_doc(doc)

@router.get("/history/{user_id}/{other_id}")
def get_history(user_id: str, other_id: str):
    """İki kullanıcı arasındaki mesajlaşma geçmişini getirir."""
    msgs = list(messages_col.find({
        "$or": [
            {"sender_id": user_id, "receiver_id": other_id},
            {"sender_id": other_id, "receiver_id": user_id}
        ]
    }).sort("created_at", 1))
    return serialize_list(msgs)

@router.get("/active-chats/{user_id}")
def get_active_chats(user_id: str):
    """Kullanıcının aktif sohbet listesini (konuştuğu kişileri) getirir."""
    sent = messages_col.distinct("receiver_id", {"sender_id": user_id})
    received = messages_col.distinct("sender_id", {"receiver_id": user_id})
    
    partner_ids = list(set(sent + received) - {user_id})
    
    partners = []
    for pid in partner_ids:
        user = users_col.find_one({"_id": ObjectId(pid)}) if ObjectId.is_valid(pid) else None
        if user:
            partners.append(serialize_doc(user))
    
    return partners
