"""
Chat Service — RAG tabanlı aday asistanı
Düzeltmeler:
  1. candidate_id: string (MongoDB ObjectId) olarak geçiriliyor
  2. rag_engine.query() metodu artık var
"""
from langchain_core.prompts import ChatPromptTemplate
from config import settings
from pymongo import MongoClient

# MongoDB bağlantısı (Adayın temel profilini ve CV metnini çekmek için)
client = MongoClient(settings.mongodb_uri)
db = client[settings.mongodb_db_name]
candidates_col = db["candidates"]


class ChatService:
    def __init__(self):
        if settings.llm_provider == "openai":
            from langchain_openai import ChatOpenAI
            self.llm = ChatOpenAI(
                model=settings.openai_model,
                api_key=settings.openai_api_key,
                temperature=0.4
            )
        elif settings.llm_provider == "gemini":
            from langchain_google_genai import ChatGoogleGenerativeAI
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=settings.google_api_key,
                temperature=0.4
            )
        else:
            from langchain_ollama import ChatOllama
            self.llm = ChatOllama(
                base_url=settings.ollama_base_url,
                model=settings.ollama_model,
                temperature=0.4
            )

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "Sen profesyonel bir İK ve Kariyer Asistanısın. "
                "Sana verilen aşağıdaki adayın temel profilini ve detaylı CV bağlamını kullanarak "
                "sorulan soruları YALNIZCA TÜRKÇE (Turkish) olarak yanıtla. "
                "HİÇBİR ŞEKİLDE Çince, İngilizce veya başka bir dil kullanma.\n\n"
                "Adayın profilinde veya CV bağlamında yer alan bilgiler KESİN olarak doğrudur. "
                "Yanıtların kısa, net, profesyonel ve kesin bir dille olsun.\n"
                "Eğer sorunun cevabı bu bağlamlarda veya adayın profilinde yoksa SADECE: 'Adayın CV'sinde bu bilgi bulunmuyor.' de.\n\n"
                "Adayın Profil ve CV Bağlamı:\n{context}"
            )),
            ("human", "{question}"),
        ])

    async def get_response(self, candidate_id: str, question: str):
        """
        RAG İPTAL: CV'nin tamamı DB'den çekilerek doğrudan LLM modeline bağlam olarak sunulur.
        """
        from bson.objectid import ObjectId
        candidate = candidates_col.find_one({"_id": ObjectId(candidate_id)})
        
        if not candidate:
            return {"response": "Aday bulunamadı.", "source": "db_error"}

        # Adayın DB'de tutulan tam CV metnini al
        full_cv_text = candidate.get("cv_text", "")
        
        # Ekstra garanti için temel bilgileri de en başa ekleyelim
        name = candidate.get("full_name", candidate.get("name", "Bilinmeyen Aday"))
        skills = ", ".join(candidate.get("skills", []))
        exp = candidate.get("experience_years", 0)
        base_info = f"Adayın Adı: {name}\nTahmini Tecrübe: {exp} yıl\nYetenekleri: {skills}\n\n[TAM CV METNİ BAŞLANGICI]\n"
        
        context_text = base_info + full_cv_text + "\n[TAM CV METNİ SONU]" if full_cv_text else base_info + "CV metni veritabanında yok."

        try:
            # 2. LLM ile yanıt üret
            response = await self.llm.ainvoke(
                self.prompt.format_messages(context=context_text, question=question)
            )

            content = response.content
            if isinstance(content, list):
                content = " ".join([
                    item.get("text", "") if isinstance(item, dict) else str(item)
                    for item in content
                ])

            return {
                "response": str(content),
                "sources": ["Tam CV Metni"]
            }

        except Exception as e:
            print(f"Chat Hatası: {e}")
            return {
                "response": "Şu an bir teknik sorun yaşıyorum. Lütfen daha sonra tekrar deneyin.",
                "sources": []
            }


chat_service = ChatService()
