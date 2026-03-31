import nltk
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------
# 1. Dokumente laden
# ---------------------------
documents = [
    "Die Deutsche Bahn bietet verschiedene Ticketoptionen für Reisende an.",
    "Verspätungen können durch Bauarbeiten oder Wetter verursacht werden.",
    "ICE-Züge sind schneller als Regionalbahnen.",
]

# ---------------------------
# 2. Chunking (NLTK)
# ---------------------------
def chunk_text(text, max_tokens=50, overlap=10):
    sentences = nltk.sent_tokenize(text)
    
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        tokens = nltk.word_tokenize(sentence)
        
        if current_length + len(tokens) > max_tokens:
            chunks.append(" ".join(current_chunk))
            
            # Overlap berücksichtigen
            current_chunk = current_chunk[-overlap:] if overlap > 0 else []
            current_length = len(current_chunk)
        
        current_chunk.append(sentence)
        current_length += len(tokens)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

# Alle Dokumente in Chunks zerlegen
all_chunks = []
for doc in documents:
    all_chunks.extend(chunk_text(doc))

# ---------------------------
# 3. Embeddings
# ---------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

chunk_embeddings = model.encode(all_chunks)

# ---------------------------
# 4. Retrieval
# ---------------------------
def retrieve(query, top_k=2):
    query_embedding = model.encode([query])
    
    similarities = cosine_similarity(query_embedding, chunk_embeddings)[0]
    
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    results = [(all_chunks[i], similarities[i]) for i in top_indices]
    return results

# ---------------------------
# 5. (Dummy) Antwortgenerierung
# ---------------------------
def answer_query(query):
    retrieved_chunks = retrieve(query)
    
    context = "\n".join([chunk for chunk, _ in retrieved_chunks])
    
    # Hier würdest du ein LLM aufrufen
    response = f"""
Frage: {query}

Kontext:
{context}

Antwort:
(Basierend auf dem Kontext generiert)
"""
    return response

# ---------------------------
# Test
# ---------------------------
query = "Warum haben Züge Verspätung?"
print(answer_query(query))