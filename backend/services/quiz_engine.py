import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import List
from config import settings

class QuizQuestion(BaseModel):
    question: str = Field(description="Soru metni")
    options: List[str] = Field(description="4 adet şık dizisi")
    correct: str = Field(description="Doğru olan şıkkın metni")

class QuizResult(BaseModel):
    questions: List[QuizQuestion]

class CandidateExtraction(BaseModel):
    name: str = Field(description="Adayın tam adı")
    skills: List[str] = Field(description="Adayın teknik ve sosyal becerileri")
    experience_years: int = Field(description="Adayın toplam mesleki tecrübe yılı (tahmini)")

class QuizEngine:
    def __init__(self):
        # Ayarlara göre LLM seçimi
        if settings.llm_provider == "openai":
            self.llm = ChatOpenAI(
                model=settings.openai_model,
                api_key=settings.openai_api_key,
                temperature=0.3
            )
        elif settings.llm_provider == "gemini":
            from langchain_google_genai import ChatGoogleGenerativeAI
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-flash-latest",
                google_api_key=settings.google_api_key,
                temperature=0.3
            )
        else:
            # Ollama fallback
            from langchain_ollama import ChatOllama
            self.llm = ChatOllama(
                base_url=settings.ollama_base_url,
                model=settings.ollama_model,
                temperature=0.3
            )

    def extract_candidate_info(self, raw_text: str) -> CandidateExtraction:
        """CV metninden adayın isim, yetenek ve deneyim yıllarını çıkarır."""
        prompt = PromptTemplate.from_template(
            "Verilen Özgeçmiş metninden adayın Adını ve Soyadını, sahip olduğu yetenekleri "
            "ve toplam tecrübesini (yıl olarak) çıkar.\n\nÖzgeçmiş Metni:\n{raw_text}"
        )
        
        chain = prompt | self.llm.with_structured_output(CandidateExtraction)
        
        try:
            return chain.invoke({"raw_text": raw_text[:3000]}) # Sadece ilk kısmı al iskele için
        except Exception as e:
            print(f"Extraction hatası: {e}")
            return CandidateExtraction(name="Bilinmiyor", skills=["Belirtilmemiş"], experience_years=0)

    def generate_quiz_from_text(self, raw_text: str, skills: List[str]) -> dict:
        """README vizyonuna uygun: CV metni ve projelerden ZORLU teknik sınav oluşturur."""
        try:
            prompt = PromptTemplate.from_template(
                "Sen uzman bir teknik mülakatçısın. Aşağıdaki özgeçmişi analiz et ve adayın belirttiği "
                "projeleri, teknik yetkinlikleri ({skills}) ve iş deneyimini gerçekten doğrulayacak "
                "5 adet ZORLU ve ÖZGÜN çoktan seçmeli soru hazırla.\n\n"
                "KURALLAR:\n"
                "1. Sorular sadece teorik değil, adayın CV'sindeki spesifik deneyimlere dokunmalı.\n"
                "2. 'Hangisi doğrudur?' gibi basit sorular yerine senaryo bazlı sorular sor.\n"
                "3. Teknik yetkinliği (Hard Skills) ve projedeki rolünü sorgula.\n"
                "4. Dil her zaman profesyonel TÜRKÇE olmalı.\n\n"
                "ÖZGEÇMİŞ METNİ:\n{raw_text}\n\n"
                "Lütfen her soru için JSON formatında 'question', 4 seçenekli 'options' ve 'correct' döndür."
            )
            
            chain = prompt | self.llm.with_structured_output(QuizResult)
            result = chain.invoke({"raw_text": raw_text[:4000], "skills": ", ".join(skills)})
            return result.dict()
        except Exception as e:
            print(f"ERROR: AI Sınav Üretme Hatası: {e}")
            return {"questions": []}

    async def generate_quiz(self, raw_text: str) -> dict:
        """Yönlendiricinin beklediği ana metod. Soruları ve doğru cevapları ayrıştırır."""
        res = self.generate_quiz_from_text(raw_text, ["Genel Yazılım"])
        
        questions = []
        correct_answers = []
        
        # Eğer AI kota hatası vb. nedeniyle boş döndüyse yedek soru ekle
        if not res.get("questions"):
            return {
                "questions": [{
                    "question_text": "⚠️ Yapay zeka servis kotası dolduğu için şu an özel sınav oluşturulamıyor. Lütfen 1 dakika sonra tekrar deneyin.",
                    "options": ["Anladım, bekleyeceğim", "Tekrar Dene", "İptal", "Devam Et"]
                }],
                "correct_answers": [0]
            }
        
        for q in res.get("questions", []):
            if not q.get("question") or not q.get("options"):
                continue
            questions.append({
                "question_text": q.get("question"),
                "options": q.get("options")
            })
            correct_text = q.get("correct")
            try:
                idx = q.get("options").index(correct_text)
            except:
                idx = 0
            correct_answers.append(idx)
            
        return {
            "questions": questions,
            "correct_answers": correct_answers
        }

quiz_engine = QuizEngine()
