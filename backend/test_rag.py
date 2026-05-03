from services.rag_engine import rag_engine
import sys
chunks = rag_engine.query("69f5df5ac0954e0a6b23364a", "bana kişi hakkında bilgi ver")
print("\n--- CHUNKS RETURNED ---")
for i, c in enumerate(chunks):
    print(f"\nChunk {i+1}:")
    print(c)
