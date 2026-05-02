"""
RAG Engine — MongoDB Atlas Vector Search
Düzeltmeler:
  1. candidate_id: int() cast kaldırıldı → string (ObjectId) olarak saklanıyor
  2. CharacterTextSplitter → RecursiveCharacterTextSplitter (chunk sınırına uyuyor)
  3. .query() metodu eklendi (chat_service bunu çağırıyor)
"""
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient
from config import settings
from typing import List
import os


class RAGEngine:
    def __init__(self):
        os.makedirs(settings.upload_dir, exist_ok=True)
        os.makedirs(settings.db_dir, exist_ok=True)

        # MongoDB Bağlantısı
        self.client = MongoClient(settings.mongodb_uri)
        self.db = self.client[settings.mongodb_db_name]
        self.collection = self.db[settings.mongodb_collection_name]

        # Embedding Modeli
        if settings.llm_provider == "gemini":
            print("LOG: Gemini Embedding kullaniliyor (768 boyut)")
            from langchain_google_genai import GoogleGenerativeAIEmbeddings
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/gemini-embedding-001",
                google_api_key=settings.google_api_key
            )
        else:
            from langchain_openai import OpenAIEmbeddings
            self.embeddings = OpenAIEmbeddings(
                model=settings.openai_embedding_model,
                api_key=settings.openai_api_key
            )

        # Atlas Vector Search
        self.vector_store = MongoDBAtlasVectorSearch(
            collection=self.collection,
            embedding=self.embeddings,
            index_name=settings.mongodb_index_name,
            text_key="text",
            embedding_key="embedding"
        )

    def index_cv(self, candidate_id: str, text: str):
        """
        CV metnini parçalara ayırır ve Atlas'a yükler.
        
        BUG FIX 1: candidate_id artık string (MongoDB ObjectId), int() cast kaldırıldı.
        BUG FIX 2: RecursiveCharacterTextSplitter chunk_size'a uyar (CharacterTextSplitter uymuyordu).
        """
        print(f"LOG: Aday {candidate_id} için Atlas indexleme basliyor...")

        # FIX 2: Recursive splitter — chunk_size'a gerçekten uyar
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=80,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        chunks = text_splitter.split_text(text)

        # FIX 1: candidate_id string olarak sakla, int() yok
        self.vector_store.add_texts(
            texts=chunks,
            metadatas=[{"candidate_id": str(candidate_id)} for _ in chunks]
        )
        print(f"LOG: Aday {candidate_id} için {len(chunks)} parça yüklendi.")

    def query(self, candidate_id: str, question: str, n_results: int = 3) -> List[str]:
        """
        chat_service'in çağırdığı metod (eski adı get_relevant_context).
        BUG FIX 3: Hem .query() hem .get_relevant_context() çalışır.
        BUG FIX 1: pre_filter'da int() cast yok, string karşılaştırma.
        """
        return self.get_relevant_context(candidate_id, question, n_results)

    def get_relevant_context(self, candidate_id: str, question: str, n_results: int = 3) -> List[str]:
        """Soruyla ilgili en alakalı CV parçalarını getirir."""
        try:
            print(f"LOG: Arama yapiliyor... AdayID: {candidate_id}, Soru: {question}")

            # FIX 1: candidate_id string olarak filtrele, int() yok
            docs = self.vector_store.similarity_search(
                query=question,
                k=n_results,
                pre_filter={"candidate_id": {"$eq": str(candidate_id)}}
            )

            # Fallback: Filtreli aramada sonuç yoksa genel arama
            if not docs:
                print("LOG: Filtreli aramada sonuç bulunamadı, genel arama deneniyor...")
                docs = self.vector_store.similarity_search(query=question, k=n_results)

            print(f"LOG: Bulunan parça sayısı: {len(docs)}")
            return [doc.page_content for doc in docs]

        except Exception as e:
            print(f"MongoDB Sorgu hatası: {e}")
            return []


rag_engine = RAGEngine()
