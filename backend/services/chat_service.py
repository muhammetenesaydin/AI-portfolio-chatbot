"""
Chat Service — RAG tabanlı aday asistanı
Düzeltmeler:
  1. candidate_id: string (MongoDB ObjectId) olarak geçiriliyor
  2. rag_engine.query() metodu artık var
"""
from langchain_core.prompts import ChatPromptTemplate
from services.rag_engine import rag_engine
from config import settings


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
            from langchain_community.chat_models import ChatOllama
            self.llm = ChatOllama(
                base_url=settings.ollama_base_url,
                model=settings.ollama_model,
                temperature=0.4
            )

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "Sen bir profesyonel kariyer asistanısın. Aşağıdaki CV bağlamını kullanarak "
                "aday hakkında sorulan soruları yanıtla. Yanıtların kısa, profesyonel ve bilgilendirici olsun.\n\n"
                "Eğer sorunun cevabı bağlamda yoksa: 'Adayın CV'sinde bu bilgi bulunmuyor.' de.\n\n"
                "CV Bağlamı:\n{context}"
            )),
            ("human", "{question}"),
        ])

    async def get_response(self, candidate_id: str, question: str):
        """
        RAG kullanarak aday hakkında soruları yanıtlar.
        FIX: candidate_id artık string (MongoDB ObjectId).
        """
        # 1. İlgili CV parçalarını getir
        context_chunks = rag_engine.query(str(candidate_id), question)
        context_text = "\n---\n".join(context_chunks) if context_chunks else "CV verisi bulunamadı."

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
                "sources": context_chunks[:2]
            }

        except Exception as e:
            print(f"Chat Hatası: {e}")
            return {
                "response": "Şu an bir teknik sorun yaşıyorum. Lütfen daha sonra tekrar deneyin.",
                "sources": []
            }


chat_service = ChatService()
