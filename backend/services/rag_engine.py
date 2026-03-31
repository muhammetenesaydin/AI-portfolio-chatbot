from langchain.text_splitter import RecursiveCharacterTextSplitter
from database import chroma_client
from config import settings

class RAGEngine:
    def __init__(self):
        self.collection = chroma_client.get_or_create_collection(name="cv_chunks")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False,
        )

        if settings.llm_provider == "openai":
            from langchain_openai import OpenAIEmbeddings
            self.embeddings = OpenAIEmbeddings(
                model=settings.openai_embedding_model,
                api_key=settings.openai_api_key
            )
        else:
            from langchain_community.embeddings import OllamaEmbeddings
            self.embeddings = OllamaEmbeddings(
                base_url=settings.ollama_base_url,
                model=settings.ollama_model
            )

    def index_cv(self, candidate_id: int, raw_text: str):
        """CV metnini parçalara ayırır (chunking) ve ChromaDB'ye vektör olarak ekler."""
        chunks = self.text_splitter.split_text(raw_text)
        
        try:
            # Generate IDs and Metadata
            ids = [f"cand_{candidate_id}_chunk_{i}" for i in range(len(chunks))]
            metadatas = [{"candidate_id": candidate_id} for _ in range(len(chunks))]
            
            # Use embeddings directly or let Chroma store it via its own embedding function 
            # (In Langchain we usually use Langchain's chroma wrapper but since we are using persistent client directly:)
            embedded_chunks = self.embeddings.embed_documents(chunks)
            
            self.collection.add(
                ids=ids,
                embeddings=embedded_chunks,
                metadatas=metadatas,
                documents=chunks
            )
            print(f"Aday {candidate_id} için {len(chunks)} chunk vektörleştirildi.")
        except Exception as e:
            print(f"Vektörleştirme hatası (Muhtemelen API key yok veya ağ sorunu): {e}")

rag_engine = RAGEngine()
