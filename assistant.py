# assistant.py
import os
import faiss
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

EMBEDDING_MODEL = "text-embedding-3-small"
CHUNK_FILE = "docs_chunks.txt"
INDEX_FILE = "docs_index.faiss"

load_dotenv()

# if in a local env, will use .env
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("❌ OPENAI_API_KEY not set")

client = OpenAI(api_key=api_key)
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-5-nano")
# use gpt-5-nano as a default value
def embed_texts(texts):
    response = client.embeddings.create(
        input=texts,
        model=EMBEDDING_MODEL
    )
    return [item.embedding for item in response.data]

def load_faiss_index():
    if not os.path.exists(INDEX_FILE) or not os.path.exists(CHUNK_FILE):
        return None, None
    try:
        index = faiss.read_index(INDEX_FILE)
    except Exception as e:
        print(f"❌ Failed to read FAISS index: {e}")
        return None, None
    with open(CHUNK_FILE, "r", encoding="utf-8") as f:
        chunks = [line.strip() for line in f if line.strip()]
    return index, chunks

def answer_query(query, threshold=0.9):
    print(f"📥 user query: {query}")
    index, chunks = load_faiss_index()

    try:
        query_vector = embed_texts([query])[0]
    except Exception as e:
        return f"❌ Failed to embed query: {e}"

    if index and chunks:
        D, I = index.search(np.array([query_vector]).astype("float32"), k=1)
        top_score = D[0][0]
        top_chunk = chunks[I[0][0]]
        print(f"📌 Top similarity distance: {top_score:.4f}")

        if top_score < threshold:
            prompt = f"根據以下文件內容回答問題：\n\n{top_chunk}\n\n問題：{query}"
        else:
            prompt = f"{query}（這是一個知識性問題，請以通用方式回答）"
    else:
        print("⚠️ 沒有找到可用文件索引，改用 fallback 模式")
        prompt = f"{query}（這是一個知識性問題，請以通用方式回答）"

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=1
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Failed to generate response: {e}"