from fastapi import FastAPI, Query
from pydantic import BaseModel
from assistant import answer_query
from mangum import Mangum

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
async def ask_endpoint(data: QueryRequest):
    answer = answer_query(data.query)
    return {"answer": answer}

@app.get("/answer")
async def answer_endpoint(query: str = Query(..., description="使用者提問")):
    answer = answer_query(query)
    return {"answer": answer}

@app.get("/")
def read_root():
    return {"message": "✅ RAG Assistant is running. Use /answer (GET) or /ask (POST)."}

# Lambda handler
handler = Mangum(app)