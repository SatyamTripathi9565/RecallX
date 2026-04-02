from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')


# 🔥 Generate embedding
def get_embedding(text):
    return model.encode(text).tolist()


# 🔥 Semantic Search (FIXED)
def search(query, memories):
    try:
        # Query embedding
        q = model.encode(query)

        results = []

        for m in memories:
            try:
                # ✅ FIX: safe JSON load (no eval)
                emb = np.array(json.loads(m.embedding))

                score = cosine_similarity([q], [emb])[0][0]

                results.append((score, m))

            except Exception as e:
                print(f"Skipping memory: {e}")

        # Sort by similarity
        results = sorted(results, key=lambda x: x[0], reverse=True)

        return [r[1] for r in results[:5]]

    except Exception as e:
        print(f"Search error: {e}")
        return []