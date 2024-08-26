from pymongo import MongoClient
import numpy as np
import faiss
from config import config
from utils.chunking import chunk_document
from utils.vectorization import vectorize_query

client = MongoClient(config.MONGO_URI)
db = client["your_database_name"]
collection = db["your_collection_name"]

def store_document(user_id: str, document: str):
    """
    Store a document in the database after chunking and vectorizing.

    Args:
        user_id (str): The ID of the user storing the document.
        document (str): The document to be stored.
    """
    chunks = chunk_document(document)
    for i, chunk in enumerate(chunks):
        vector = vectorize_query(chunk)
        collection.insert_one({
            "user_id": user_id,
            "chunk": chunk,
            "vector": vector,
            "index": i
        })

def process_query(user_id: str, query_vector: np.ndarray) -> list:
    """
    Process a user query and return relevant chunks.

    Args:
        user_id (str): The ID of the user making the query.
        query_vector (np.ndarray): The vector representation of the query.

    Returns:
        list: A list of search results with document chunks and scores.
    """
    # Fetch vectors and chunks from MongoDB
    documents = list(collection.find({"user_id": user_id}))
    if not documents:
        return []

    vectors = np.array([doc["vector"] for doc in documents])
    chunks = [doc["chunk"] for doc in documents]
    
    # Create FAISS index and search
    d = vectors.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(vectors)
    query_vector = np.expand_dims(query_vector, axis=0)
    distances, indices = index.search(query_vector, k=5)

    # Retrieve documents based on indices
    results = []
    for idx in indices[0]:
        doc = documents[idx]
        results.append({
            "document_id": doc.get("_id"),
            "chunk": doc.get("chunk"),
            "score": 1 / (1 + distances[0][idx])
        })

    return results
