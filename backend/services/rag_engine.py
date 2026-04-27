from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from typing import List
from langchain_text_splitters import CharacterTextSplitter
from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient
from config import settings

class RAGEngine:
    def __init__(self):
        # Klasörleri oluştur
        os.makedirs(settings.upload_dir, exist_ok=True)
        os.makedirs(settings.db_dir, exist_ok=True)
        
        # 1. MongoDB Bağlantısı
        self.client = MongoClient(settings.mongodb_uri)
        self.db = self.client[settings.mongodb_db_name]
        self.collection = self.db[settings.mongodb_collection_name]

        # 2. Embedding Modeli
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

        # 3. Atlas Vector Search Nesnesi
        self.vector_store = MongoDBAtlasVectorSearch(
            collection=self.collection,
            embedding=self.embeddings,
            index_name=settings.mongodb_index_name,
            text_key="text",
            embedding_key="embedding"
        )

    def index_cv(self, candidate_id: int, text: str):
        """CV metnini parçalara ayırır ve Atlas'a yükler."""
        print(f"LOG: Aday {candidate_id} için Atlas indexleme basliyor...")
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_text(text)
        
        self.vector_store.add_texts(
            texts=chunks,
            metadatas=[{"candidate_id": int(candidate_id)} for _ in chunks]
        )
        print(f"LOG: Aday {candidate_id} için {len(chunks)} parça yüklendi.")

    def get_relevant_context(self, candidate_id: int, question: str, n_results: int = 3) -> List[str]:
        """Soruyla ilgili en alakalı CV parçalarını getirir."""
        try:
            print(f"LOG: Arama yapiliyor... AdayID: {candidate_id}, Soru: {question}")
            
            # 1. Filtreli Arama Dene
            docs = self.vector_store.similarity_search(
                query=question,
                k=n_results,
                pre_filter={"candidate_id": {"$eq": int(candidate_id)}}
            )
            
            # 2. Eğer sonuç yoksa, filtreyi gevşet (Fallback)
            if not docs:
                print("LOG: Filtreli aramada sonuç bulunamadı, genel arama deneniyor...")
                docs = self.vector_store.similarity_search(query=question, k=n_results)
            
            print(f"LOG: Bulunan parça sayısı: {len(docs)}")
            return [doc.page_content for doc in docs]
        except Exception as e:
            print(f"MongoDB Sorgu hatası: {e}")
            return []

rag_engine = RAGEngine()
