import faiss
import numpy as np

def create_index(vectors: np.ndarray) -> faiss.Index:
    d = vectors.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(vectors)
    return index

def search_index(index: faiss.Index, query_vector: np.ndarray, k: int = 5) -> list:
    distances, indices = index.search(query_vector, k)
    return indices[0]
