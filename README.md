# 🧠 AI RAG Assistant on AWS Lambda (FastAPI + FAISS)

This is a lightweight AI document assistant that answers questions based on **uploaded documents**, using OpenAI's embedding + retrieval mechanism.

> ✅ Fully containerized for deployment on **AWS Lambda with ECR**, powered by **FastAPI + Mangum**.

---

## 🚀 Features

- Embed text using `text-embedding-3-small`
- Query via FAISS vector search
- RAG fallback: switch to GPT if no match is found
- REST API with:
  - `GET /answer?query=...`
  - `POST /ask` with JSON body
- Deployed on AWS Lambda using container image

---

## 🧩 File Structure

| File | Description |
|------|-------------|
| `assistant.py` | Core logic: load FAISS index, embed query, match, call GPT |
| `main.py`      | FastAPI server with `/ask` and `/answer` endpoints |
| `Dockerfile`   | Slim image with Python 3.10, FastAPI, FAISS |
| `docs_index.faiss` | FAISS binary index of embedded docs |
| `docs_chunks.txt`  | Raw text chunks for index-to-text mapping |
| `.env.example` | Sample environment variables |
| `requirements.txt` | Python deps |

---

## 🔧 How to Run Locally

```bash
# 1. Clone repo
git clone https://github.com/yourname/ai-rag-assistant.git

# 2. Set environment
cp .env.example .env
# Edit your OpenAI key

# 3. Build & run
docker build -t rag-assistant .
docker run --env-file .env -p 8000:8000 rag-assistant

## 🐛 Known Issues (Lambda)

- ❗ `Runtime.InvalidEntrypoint` on AWS Lambda: likely due to CMD format or FastAPI-Mangum binding error.
- ❗ `UnrecognizedClientException` caused by temporary AWS credentials issue in `~/.aws/config`.

## 🧭 Future Work

- PDF / CSV ingestion
- CI/CD deployment using GitHub Actions
- Switch to local LLM model + OpenRouter for lower-cost inference
- Frontend UI (Next.js)
