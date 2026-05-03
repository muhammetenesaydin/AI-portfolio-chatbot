from pymongo import MongoClient
from config import settings
from langchain_ollama import OllamaEmbeddings

client = MongoClient(settings.mongodb_uri)
col = client[settings.mongodb_db_name][settings.mongodb_collection_name]

# Generate a query embedding
emb = OllamaEmbeddings(base_url=settings.ollama_base_url, model="nomic-embed-text")
query_vector = emb.embed_query("aday ros biliyor mu")

print("Query vector size:", len(query_vector))
print("First 5:", query_vector[:5])

# Run Atlas Vector Search
results = col.aggregate([
    {
        "$vectorSearch": {
            "index": settings.mongodb_index_name,
            "path": "embedding",
            "queryVector": query_vector,
            "numCandidates": 100,
            "limit": 3
        }
    }
])

docs = list(results)
print("Docs found:", len(docs))
if docs:
    print("Score:", docs[0].get("score"))
