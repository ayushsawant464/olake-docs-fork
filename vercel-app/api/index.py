"""
Vercel Serverless Function & FastAPI Entrypoint for OLake Docs Assistant.
Endpoints:
- POST /api/ask (and /ask): Generates answer grounded by OLake docs using OpenRouter API.
- GET /api/health (and /health): Healthcheck endpoint.
"""

import os
import json
import requests
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from .docs_engine import ServerlessDocsMemory

app = FastAPI(title="OLake Docs Assistant API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
HARNESS_PATH = os.path.join(BASE_DIR, "harness", "harness.md")

# Initialize docs engine
docs_memory = ServerlessDocsMemory(docs_path=DOCS_DIR)

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
BASE_URL = "https://openrouter.ai/api/v1"
PRIMARY_MODEL = os.environ.get("MODEL", "z-ai/glm-4.7-flash")
FALLBACK_MODELS = ["google/gemini-2.5-flash-lite", "deepseek/deepseek-v4.1-flash"]

def get_harness() -> str:
    if os.path.exists(HARNESS_PATH):
        try:
            with open(HARNESS_PATH, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            pass
    return "You are the official OLake documentation assistant. Answer questions strictly based on the provided docs."

class AskRequest(BaseModel):
    question: str

@app.get("/")
@app.get("/api/health")
@app.get("/health")
def health():
    return {
        "status": "ok",
        "docs_indexed": len(docs_memory.docs),
        "primary_model": PRIMARY_MODEL
    }

@app.post("/ask")
@app.post("/api/ask")
def ask(req: AskRequest):
    question = req.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    api_key = os.environ.get("OPENROUTER_API_KEY", OPENROUTER_API_KEY)
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENROUTER_API_KEY environment variable is not configured in Vercel settings."
        )

    # 1. Retrieve top matching docs
    results = docs_memory.search_docs(question, limit=4)
    sources = [r["path"] for r in results]

    # 2. Build full context for synthesizer
    context_blocks = []
    for r in results:
        content = r.get("content", "")[:3500]
        context_blocks.append(f"### Source: {r['path']}\n```markdown\n{content}\n```")

    context_str = "\n\n".join(context_blocks) if context_blocks else "No matching documentation found."

    harness = get_harness()
    system_prompt = f"""{harness}

## Retrieved Documentation Context:
{context_str}
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Answer the following question comprehensively based on the retrieved documentation context:\n\"{question}\"\nRemember to cite your source documents and clearly state when something is not documented or unanswerable."}
    ]

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": PRIMARY_MODEL,
        "models": FALLBACK_MODELS,
        "messages": messages,
        "max_tokens": 600,
        "reasoning": {"effort": "none"}
    }

    try:
        res = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=payload, timeout=30)
        if res.status_code != 200:
            if "reasoning" in res.text:
                payload.pop("reasoning", None)
                res = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=payload, timeout=30)

        if res.status_code != 200:
            raise HTTPException(status_code=502, detail=f"OpenRouter API error {res.status_code}: {res.text}")

        data = res.json()
        answer = data["choices"][0]["message"].get("content", "") or "No response generated."
        model_used = data.get("model", PRIMARY_MODEL)

        return {
            "answer": answer,
            "sources": sources,
            "model": model_used
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process query: {str(e)}")
