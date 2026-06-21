# 🤖 NoumanBot – Personal RAG Chatbot

**NLP Semester Project | CC438 | UMT Lahore | Spring 2026**

A Retrieval-Augmented Generation (RAG) chatbot built with LangChain, FAISS, Groq LLaMA 3, and Streamlit.

---

## 🚀 Features

- ✅ Personal knowledge base (your own documents)
- ✅ FAISS vector store for fast semantic retrieval
- ✅ Groq LLaMA 3 for lightning-fast LLM responses
- ✅ Conversation history (last 6 exchanges remembered)
- ✅ Upload your own PDF/TXT files at runtime
- ✅ Beautiful dark-mode Streamlit UI
- ✅ Deployed on Streamlit Cloud

---

## 📁 Project Structure

```
rag_chatbot/
├── app.py                  # Streamlit frontend
├── rag_pipeline.py         # RAG core (load, embed, retrieve, generate)
├── data/
│   └── personal_knowledge.txt  # Your personal dataset
├── requirements.txt
├── .env                    # API keys (NOT committed to Git)
├── .gitignore
└── README.md
```

---

## ⚙️ Setup & Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/your-username/alibot.git
cd alibot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your API key
Edit the `.env` file:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get a free key at: https://console.groq.com

### 4. Add your personal data
Place `.txt` or `.pdf` files inside the `data/` folder.

### 5. Run
```bash
streamlit run app.py
```

---

## ☁️ Deploy on Streamlit Cloud

1. Push your code to GitHub (make sure `.env` is in `.gitignore`)
2. Go to https://share.streamlit.io → **New app**
3. Select your repo, branch `main`, and file `app.py`
4. Go to **Advanced settings → Secrets** and add:
   ```toml
   GROQ_API_KEY = "gsk_your_actual_key_here"
   ```
5. Click **Deploy** — done! 🎉

---

## 🛠️ Tech Stack

| Component         | Technology                          |
|-------------------|-------------------------------------|
| LLM               | Groq LLaMA 3 8B (llama3-8b-8192)   |
| Embeddings        | sentence-transformers/all-MiniLM-L6-v2 |
| Vector Store      | FAISS (local)                       |
| RAG Framework     | LangChain                           |
| Frontend          | Streamlit                           |
| Deployment        | Streamlit Cloud                     |

---

## 📌 How It Works

1. **Document Loading** – Reads `.txt` and `.pdf` files from the `data/` folder
2. **Chunking** – Splits documents into 500-token overlapping chunks
3. **Embedding** – Converts chunks into vectors using MiniLM
4. **FAISS Index** – Stores vectors for fast similarity search
5. **Retrieval** – Fetches top-4 relevant chunks for each query
6. **Generation** – Groq LLaMA 3 generates a context-aware response
7. **Memory** – Keeps the last 6 conversation turns in memory

---

## 📝 Dataset

The personal knowledge base includes:
- Personal bio, education details
- Technical skills and certifications
- Project descriptions
- Work experience and goals

You can extend it by uploading more files via the sidebar.

---

*Built for NLP Course CC438 — Individual Project*
