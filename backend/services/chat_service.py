from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from services.rag_engine import rag_engine
from config import settings

class ChatService:
    def __init__(self):
        if settings.llm_provider == "openai":
            self.llm = ChatOpenAI(
                model=settings.openai_model,
                api_key=settings.openai_api_key,
                temperature=0.4
            )
        elif settings.llm_provider == "gemini":
            from langchain_google_genai import ChatGoogleGenerativeAI
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-flash-latest",
                google_api_key=settings.google_api_key,
                temperature=0.4
            )
        else:
            from langchain_community.chat_models import ChatOllama
            self.llm = ChatOllama(
                base_url=settings.ollama_base_url,
                model=settings.ollama_model,
                temperature=0.4
            )

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "Sen bir profesyonel kariyer asistanısın. Aşağıdaki bağlam (context) bilgilerini kullanarak "
                "ilgili aday hakkında sorulan soruları yanıtla. Yanıtların nazik, profesyonel ve bilgilendirici olsun.\n\n"
                "Eğer sorulan sorunun cevabı bağlam içinde yoksa, adayın bu konuda bilgi vermediğini "
                "ancak genel profesyonel profilinin güçlü olduğunu belirterek nazikçe cevap ver.\n\n"
                "Bağlam Bilgisi:\n{context}"
            )),
            ("human", "{question}"),
        ])

    async def get_response(self, candidate_id: int, question: str):
        """RAG kullanarak aday hakkında soru cevaplar."""
        # 1. Benzer metinleri getir (Retrieval)
        context_chunks = rag_engine.query(candidate_id, question)
        context_text = "\n---\n".join(context_chunks)

        # 2. LLM Zincirini oluştur ve çalıştır (Generation)
        chain = self.prompt | self.llm
        
        try:
            response = await self.llm.ainvoke(
                self.prompt.format_messages(context=context_text, question=question)
            )
            
            # AIMessage'dan içeriği al
            content = response.content
            
            # Eğer içerik listeyse (bazı Gemini yanıtlarında olduğu gibi), metni birleştir
            if isinstance(content, list):
                content = " ".join([item.get("text", "") if isinstance(item, dict) else str(item) for item in content])
            
            return {
                "response": str(content),
                "sources": context_chunks[:2] # İlk 2 kaynağı göster
            }
        except Exception as e:
            print(f"Chat Hatası: {e}")
            return {
                "response": "Üzgünüm, şu an adayın profil bilgilerine ulaşırken bir teknik sorun yaşıyorum. Lütfen daha sonra tekrar deneyin.",
                "sources": []
            }

chat_service = ChatService()
