# OLake In-App Documentation Assistant – Vercel Deployment Guide

This package provides a standalone, production-ready Vercel deployment of the OLake AI Documentation Chatbot with:
- **FastAPI Serverless Backend** (`api/index.py`)
- **In-Memory BM25 Docs Retrieval** (`api/docs_engine.py`)
- **Full-Context Synthesizer** powered by OpenRouter (`z-ai/glm-4.7-flash`, `google/gemini-2.5-flash-lite`, `deepseek/deepseek-v4.1-flash`)
- **Interactive Dark-Mode Web Chat UI** (`public/index.html`)

---

## 🚀 Quick Deployment Options

### Option 1: Deploy with Vercel CLI (Recommended – 60 seconds)

1. **Install Vercel CLI (if not already installed):**
   ```bash
   npm install -g vercel
   ```

2. **Navigate into the `vercel-app` folder:**
   ```bash
   cd vercel-app
   ```

3. **Deploy directly:**
   ```bash
   vercel
   ```
   Follow the prompts (accept default settings).

4. **Set your OpenRouter API Key in Vercel:**
   ```bash
   vercel env add OPENROUTER_API_KEY
   ```
   Enter your key starting with `sk-or-v1-...` and select `Production`, `Preview`, and `Development`.

5. **Deploy to production:**
   ```bash
   vercel --prod
   ```
   Your live chat UI will be available at: `https://your-project.vercel.app`!

---

### Option 2: Deploy via GitHub (Vercel Web Dashboard)

1. **Push this repository to GitHub.**
2. Go to [vercel.com/new](https://vercel.com/new) and import your repository.
3. In the **Configure Project** screen:
   - **Root Directory:** Click "Edit" and choose `vercel-app`.
   - **Framework Preset:** Choose **Other**.
4. In **Environment Variables**, add:
   - Key: `OPENROUTER_API_KEY`
   - Value: `sk-or-v1-...` (your OpenRouter key)
5. Click **Deploy**. Vercel will build the serverless functions and host the static UI.

---

## 💻 Local Testing (Direct Python, No Container)

To test locally without Docker or containers:

1. **Install dependencies:**
   ```bash
   pip install -r vercel-app/requirements.txt
   ```

2. **Set your API Key:**
   ```bash
   export OPENROUTER_API_KEY="sk-or-v1-..."
   ```

3. **Run the local development server:**
   ```bash
   uvicorn vercel-app.api.index:app --reload --port 3000
   ```

4. **Open your browser:**
   - Web Chat UI: `http://localhost:3000/`
   - API Ask Endpoint: `POST http://localhost:3000/api/ask`
   - Healthcheck: `http://localhost:3000/api/health`

---

## 📡 API Specification

### `POST /api/ask`
**Request:**
```json
{
  "question": "How do I set up logical replication in PostgreSQL for CDC?"
}
```

**Response:**
```json
{
  "answer": "To set up logical replication in PostgreSQL for OLake CDC:\n\n1. Set `wal_level = logical` in `postgresql.conf`...\n\n**Source**: `docs/connectors/postgres/index.mdx`",
  "sources": [
    "docs/connectors/postgres/index.mdx"
  ],
  "model": "z-ai/glm-4.7-flash"
}
```
