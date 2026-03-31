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
        else:
            # Ollama fallback fallback
            from langchain_community.chat_models import ChatOllama
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
        """CV metni ve yeteneklerden teknik sınav (quiz) oluşturur."""
        prompt = PromptTemplate.from_template(
            "Aşağıdaki özgeçmiş metninde yer alan tecrübe ve yeteneklere ({skills}) göre adayı test edecek "
            "teknik ve davranışsal çoktan seçmeli 5 adet zorlu mülakat sorusu oluştur.\n\n"
            "Özgeçmiş Özeti:\n{raw_text}\n\n"
            "Lütfen her soru için 'question', 4 seçenekli 'options' ve doğru cevabı içeren 'correct' formatını döndür."
        )
        
        chain = prompt | self.llm.with_structured_output(QuizResult)
        
        try:
            result = chain.invoke({"raw_text": raw_text[:4000], "skills": ", ".join(skills)})
            return result.dict()
        except Exception as e:
            print(f"Quiz oluşturma hatası: {e}")
            return {
                "questions": [
                    {
                        "question": "Sistem API hatası nedeniyle quiz oluşturulamadı. (OpenAI API anahtarınızı kontrol edin)",
                        "options": ["Tamam", "Tekrar Dene", "Atla", "Kapat"],
                        "correct": "Tamam"
                    }
                ]
            }

quiz_engine = QuizEngine()
