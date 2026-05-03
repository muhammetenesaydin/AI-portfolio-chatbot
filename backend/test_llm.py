import asyncio
from services.chat_service import chat_service
from config import settings

async def main():
    print("Ollama URL:", settings.ollama_base_url)
    from pymongo import MongoClient
    from bson.objectid import ObjectId
    client = MongoClient(settings.mongodb_uri)
    db = client[settings.mongodb_db_name]
    candidate = db["candidates"].find_one({"_id": ObjectId("69f5df5ac0954e0a6b23364a")})
    print("Candidate fetched manually:", candidate)
    
    res = await chat_service.get_response("69f5df5ac0954e0a6b23364a", "bana kişi hakkında bilgi ver")
    print("--- RESPONSE ---")
    print(res["response"])

asyncio.run(main())
