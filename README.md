# ⬡ DocMind Hybrid AI
### Enterprise Financial Intelligence Platform

> Bloomberg Terminal × Palantir × Modern AI — precision hybrid search over your documents.

![DocMind](https://img.shields.io/badge/DocMind-Hybrid%20AI-22D3EE?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=for-the-badge&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python)

---

## 🚀 Features

- **Hybrid Search** — Dense (semantic) + Sparse (BM25) + RRF fusion
- **Multi-Model** — Llama 3.3 70B, Gemini 2.0 Flash, DeepSeek R1 (Financial)
- **Financial Mode** — Numerical precision, calculation verification, gold accents
- **Source Citations** — Every answer linked to exact document passages with relevance scores
- **Institutional UI** — Dark terminal aesthetic, IBM Plex Mono, Source Serif Pro
- **Free Tier** — All APIs on free tiers (Groq, Gemini, Pinecone)

---

## 📋 Setup Instructions

### 1. Fork / Clone this repo to GitHub

```bash
git clone https://github.com/YOUR_USERNAME/docmind-hybrid-ai
cd docmind-hybrid-ai
```

### 2. Get your FREE API Keys

| Service | URL | Free Tier |
|---------|-----|-----------|
| **Groq** (Llama + DeepSeek) | https://console.groq.com | 30 req/min |
| **Google Gemini** | https://aistudio.google.com/app/apikey | 15 req/min |
| **Pinecone** | https://app.pinecone.io | 1 index, 100k vectors |

### 3. Deploy to Streamlit Cloud

1. Go to **https://share.streamlit.io**
2. Click **"New app"**
3. Connect your GitHub repo
4. Set **Main file path**: `app.py`
5. Click **"Advanced settings" → Secrets**
6. Add your secrets (see below)
7. Click **Deploy!**

### 4. Add Secrets in Streamlit Cloud

In **App Settings → Secrets**, paste:

```toml
GROQ_API_KEY = "gsk_your_groq_key_here"
GEMINI_API_KEY = "AIza_your_gemini_key_here"
PINECONE_API_KEY = "your_pinecone_key_here"
PINECONE_INDEX_NAME = "docmind-index"
```

> **Note:** App works without Pinecone (uses local in-memory search). Add Pinecone for persistence across sessions.

---

## 🏗️ Architecture

```
User Query
    │
    ├── Dense Search (BAAI/bge-small-en-v1.5 embeddings → Pinecone or local)
    │
    ├── Sparse Search (BM25 Okapi → in-memory)
    │
    └── RRF Fusion → Top-K chunks
              │
              └── LLM Generation (Groq / Gemini)
                        │
                        └── Response + Source Citations
```

### Models

| Model | Provider | Best For |
|-------|----------|----------|
| Llama 3.3 70B | Groq | General Q&A, fast responses |
| Gemini 2.0 Flash | Google | Long reports, structured output |
| DeepSeek R1 Distill | Groq | Financial analysis, reasoning |

---

## 📁 File Structure

```
docmind-hybrid-ai/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── config.toml          # Streamlit theme config
└── README.md
```

---

## 🔧 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "GROQ_API_KEY=your_key" > .env
echo "GEMINI_API_KEY=your_key" >> .env

# Run
streamlit run app.py
```

---

## ⚡ Performance Notes

- **First load:** ~30-60s to download embedding model (BAAI/bge-small-en-v1.5, ~130MB)
- **Subsequent loads:** Cached by Streamlit
- **Large PDFs:** 100-page PDF ≈ 15-30 seconds to index
- **Pinecone:** Recommended for documents > 50 pages or multi-session use

---

## 🎨 Design System

- **Colors:** Deep navy base, cyan accents, gold for financial mode
- **Fonts:** IBM Plex Mono (headers) · Inter (UI) · Source Serif 4 (responses) · JetBrains Mono (data)
- **Inspiration:** Bloomberg Terminal × Palantir × Modern data platforms

---

## 📝 Usage Tips

1. **Upload documents** via the sidebar (PDF, TXT, DOCX)
2. **Select model** based on your task (DeepSeek for financials)
3. **Set mode** (Financial Analysis for numerical precision)
4. **Adjust k** (retrieved chunks) — higher = more context, slower
5. **Use Hybrid search** for best results (default)

---

## ⚠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| "No API key" warning | Add keys to Streamlit Secrets |
| Slow first response | Embedding model loading — wait 30-60s |
| Empty responses | Check if documents are uploaded and indexed |
| Pinecone error | App falls back to local search automatically |
| Rate limit error | Switch to a different model, or wait 1 minute |

---

*Built with ❤️ using Streamlit · Groq · Pinecone · sentence-transformers*
