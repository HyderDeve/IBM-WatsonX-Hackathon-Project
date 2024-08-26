from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from utils.vectorization import vectorize_query
from utils.search import process_query
from config import config

app = FastAPI()

class QueryRequest(BaseModel):
    user_id: str
    query: str

class QueryResponse(BaseModel):
    user_id: str
    results: List[dict]

@app.post("/search", response_model=QueryResponse)
async def search_documents(query: QueryRequest):
    # Vectorize the query using the IBM Watson model
    query_vector = vectorize_query(query.query)

    # Process the query and get search results
    search_results = process_query(query.user_id, query_vector)

    return QueryResponse(user_id=query.user_id, results=search_results)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
