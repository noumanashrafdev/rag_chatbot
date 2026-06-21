# """
# app.py  –  NoumanBot: Personal RAG Chatbot
# Streamlit frontend with a modern, polished UI
# """

# import os
# import time
# import streamlit as st
# from pathlib import Path
# from dotenv import load_dotenv

# load_dotenv()

# # ── Page config (must be first Streamlit call) ─────────────────────────────
# st.set_page_config(
#     page_title="NoumanBot – Personal AI Assistant",
#     page_icon="🤖",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# # ── Custom CSS ──────────────────────────────────────────────────────────────
# st.markdown("""
# <style>
# /* ── Google Font ── */
# @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');

# /* ── Root palette ── */
# :root {
#     --bg:        #0d1117;
#     --surface:   #161b22;
#     --border:    #30363d;
#     --accent:    #7c3aed;
#     --accent2:   #a78bfa;
#     --text:      #e6edf3;
#     --subtext:   #8b949e;
#     --user-bg:   #1c2333;
#     --bot-bg:    #161b22;
#     --success:   #3fb950;
#     --warn:      #d29922;
# }

# /* ── Global ── */
# html, body, [class*="css"] {
#     font-family: 'Inter', sans-serif;
#     background-color: var(--bg) !important;
#     color: var(--text) !important;
# }

# /* ── Hide Streamlit chrome ── */
# #MainMenu, footer, header { visibility: hidden; }
# .stDeployButton { display: none; }
# .block-container { padding: 1rem 2rem 2rem 2rem !important; max-width: 900px; margin: 0 auto; }

# /* ── Sidebar ── */
# [data-testid="stSidebar"] {
#     background-color: var(--surface) !important;
#     border-right: 1px solid var(--border) !important;
# }
# [data-testid="stSidebar"] .stMarkdown p { color: var(--subtext); font-size: 0.85rem; }

# /* ── Header banner ── */
# .alibot-header {
#     background: linear-gradient(135deg, #1a0533 0%, #0d1117 50%, #0a1628 100%);
#     border: 1px solid var(--border);
#     border-radius: 16px;
#     padding: 2rem 2.5rem;
#     margin-bottom: 1.5rem;
#     position: relative;
#     overflow: hidden;
# }
# .alibot-header::before {
#     content: '';
#     position: absolute; top: 0; left: 0; right: 0; bottom: 0;
#     background: radial-gradient(ellipse at 20% 50%, rgba(124,58,237,0.15) 0%, transparent 60%);
#     pointer-events: none;
# }
# .alibot-header h1 {
#     font-family: 'Space Grotesk', sans-serif;
#     font-size: 2.2rem;
#     font-weight: 700;
#     margin: 0 0 0.3rem 0;
#     background: linear-gradient(90deg, #a78bfa, #60a5fa);
#     -webkit-background-clip: text;
#     -webkit-text-fill-color: transparent;
#     background-clip: text;
# }
# .alibot-header p { color: var(--subtext); margin: 0; font-size: 0.95rem; }
# .status-dot {
#     display: inline-block;
#     width: 10px; height: 10px;
#     background: var(--success);
#     border-radius: 50%;
#     margin-right: 6px;
#     animation: pulse 2s infinite;
# }
# @keyframes pulse {
#     0%, 100% { opacity: 1; }
#     50%       { opacity: 0.4; }
# }

# /* ── Chat container ── */
# .chat-wrapper {
#     display: flex;
#     flex-direction: column;
#     gap: 1rem;
#     max-height: 60vh;
#     overflow-y: auto;
#     padding: 0.5rem 0;
#     scroll-behavior: smooth;
# }

# /* ── Chat bubbles ── */
# .msg-row { display: flex; gap: 12px; align-items: flex-start; }
# .msg-row.user  { flex-direction: row-reverse; }
# .avatar {
#     width: 36px; height: 36px; border-radius: 50%;
#     display: flex; align-items: center; justify-content: center;
#     font-size: 1.1rem; flex-shrink: 0;
# }
# .avatar.bot  { background: linear-gradient(135deg, #7c3aed, #4f46e5); }
# .avatar.user { background: linear-gradient(135deg, #0ea5e9, #06b6d4); }
# .bubble {
#     max-width: 75%;
#     padding: 0.85rem 1.1rem;
#     border-radius: 16px;
#     font-size: 0.93rem;
#     line-height: 1.6;
#     border: 1px solid var(--border);
# }
# .bubble.bot  {
#     background: var(--bot-bg);
#     border-top-left-radius: 4px;
# }
# .bubble.user {
#     background: var(--user-bg);
#     border-top-right-radius: 4px;
# }
# .bubble .timestamp { font-size: 0.72rem; color: var(--subtext); margin-top: 6px; }
# .bubble .sources-tag {
#     display: inline-block;
#     font-size: 0.72rem;
#     background: rgba(124,58,237,0.2);
#     color: var(--accent2);
#     border: 1px solid rgba(124,58,237,0.3);
#     border-radius: 4px;
#     padding: 1px 6px;
#     margin-top: 6px;
# }

# /* ── Input area ── */
# .stTextInput > div > div > input {
#     background: var(--surface) !important;
#     border: 1px solid var(--border) !important;
#     border-radius: 12px !important;
#     color: var(--text) !important;
#     padding: 0.75rem 1rem !important;
#     font-size: 0.95rem !important;
#     transition: border-color 0.2s;
# }
# .stTextInput > div > div > input:focus {
#     border-color: var(--accent) !important;
#     box-shadow: 0 0 0 3px rgba(124,58,237,0.15) !important;
# }

# /* ── Buttons ── */
# .stButton > button {
#     background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
#     color: white !important;
#     border: none !important;
#     border-radius: 10px !important;
#     padding: 0.6rem 1.4rem !important;
#     font-weight: 600 !important;
#     font-size: 0.9rem !important;
#     transition: opacity 0.2s, transform 0.1s !important;
#     width: 100% !important;
# }
# .stButton > button:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }
# .stButton > button:active { transform: translateY(0) !important; }

# /* ── Stats cards ── */
# .stat-card {
#     background: var(--surface);
#     border: 1px solid var(--border);
#     border-radius: 12px;
#     padding: 1rem;
#     text-align: center;
# }
# .stat-card .val { font-size: 1.6rem; font-weight: 700; color: var(--accent2); }
# .stat-card .lbl { font-size: 0.78rem; color: var(--subtext); margin-top: 2px; }

# /* ── Divider ── */
# hr { border-color: var(--border) !important; margin: 1rem 0 !important; }

# /* ── Spinner ── */
# .stSpinner > div { border-top-color: var(--accent) !important; }

# /* ── File uploader ── */
# [data-testid="stFileUploader"] {
#     border: 1.5px dashed var(--border) !important;
#     border-radius: 12px !important;
#     background: var(--surface) !important;
#     padding: 1rem !important;
# }

# /* ── Alerts ── */
# .stAlert { border-radius: 10px !important; }

# /* ── Scrollbar ── */
# ::-webkit-scrollbar { width: 6px; }
# ::-webkit-scrollbar-track { background: transparent; }
# ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
# </style>
# """, unsafe_allow_html=True)


# # ── Lazy imports (avoid loading heavy libs until needed) ────────────────────
# @st.cache_resource(show_spinner=False)
# def init_rag(api_key: str):
#     from rag_pipeline import get_retriever, build_rag_chain
#     retriever = get_retriever()
#     chain     = build_rag_chain(retriever, api_key)
#     return chain


# # ── Session state defaults ──────────────────────────────────────────────────
# def init_state():
#     defaults = {
#         "messages":      [],   # list of {"role","content","sources","time"}
#         "chain":         None,
#         "ready":         False,
#         "total_queries": 0,
#     }
#     for k, v in defaults.items():
#         if k not in st.session_state:
#             st.session_state[k] = v

# init_state()


# # ────────────────────────────────────────────────────────────────────────────
# # SIDEBAR
# # ────────────────────────────────────────────────────────────────────────────
# with st.sidebar:
#     st.markdown("## ⚙️ Configuration")
#     st.markdown("---")

#     # API key input
#     api_key = st.text_input(
#         "🔑 Groq API Key",
#         type="password",
#         value=os.getenv("GROQ_API_KEY", ""),
#         placeholder="gsk_...",
#         help="Get your free key at console.groq.com",
#     )

#     # Upload extra docs
#     st.markdown("### 📂 Add Your Documents")
#     uploaded = st.file_uploader(
#         "Upload .txt or .pdf files",
#         accept_multiple_files=True,
#         type=["txt", "pdf"],
#         help="These are added to your personal knowledge base",
#     )
#     if uploaded:
#         data_dir = Path("data")
#         data_dir.mkdir(exist_ok=True)
#         for f in uploaded:
#             (data_dir / f.name).write_bytes(f.read())
#         st.success(f"✅ {len(uploaded)} file(s) added to knowledge base")
#         # Force re-initialization with new docs
#         init_rag.clear()
#         st.session_state.chain = None
#         st.session_state.ready = False

#     st.markdown("---")

#     # Initialize button
#     if st.button("🚀 Initialize NoumanBot", use_container_width=True):
#         if not api_key:
#             st.error("Please enter your Groq API key first.")
#         else:
#             with st.spinner("Loading knowledge base & building index…"):
#                 try:
#                     st.session_state.chain = init_rag(api_key)
#                     st.session_state.ready = True
#                     st.success("NoumanBot is ready!")
#                 except Exception as e:
#                     st.error(f"Initialization failed: {e}")

#     # Clear chat
#     if st.button("🗑️ Clear Chat History", use_container_width=True):
#         st.session_state.messages = []
#         st.session_state.total_queries = 0
#         st.rerun()

#     st.markdown("---")

#     # Stats
#     st.markdown("### 📊 Session Stats")
#     c1, c2 = st.columns(2)
#     with c1:
#         st.markdown(f"""<div class="stat-card"><div class="val">{st.session_state.total_queries}</div>
#         <div class="lbl">Queries</div></div>""", unsafe_allow_html=True)
#     with c2:
#         st.markdown(f"""<div class="stat-card"><div class="val">{len(st.session_state.messages)}</div>
#         <div class="lbl">Messages</div></div>""", unsafe_allow_html=True)

#     st.markdown("---")
#     st.markdown("""
# <div style="font-size:0.78rem; color:#8b949e;">
# <b>NoumanBot</b> — Personal RAG Chatbot<br>
# NLP Course (CC438) · UMT Lahore · Spring 2026<br><br>
# Powered by <b>LangChain · FAISS · Groq LLaMA 3 · Streamlit</b>
# </div>
# """, unsafe_allow_html=True)


# # ────────────────────────────────────────────────────────────────────────────
# # MAIN AREA
# # ────────────────────────────────────────────────────────────────────────────

# # Header
# status_html = '<span class="status-dot"></span>Online' if st.session_state.ready else '⏸ Not initialized'
# st.markdown(f"""
# <div class="alibot-header">
#   <h1>🤖 NoumanBot</h1>
#   <p>Personal AI Assistant · Nouman Ashraf · UMT Lahore</p>
#   <p style="margin-top:8px; font-size:0.82rem;">{status_html}</p>
# </div>
# """, unsafe_allow_html=True)


# # Welcome message (shown when chat is empty)
# if not st.session_state.messages:
#     st.markdown("""
# <div style="background:#161b22; border:1px solid #30363d; border-radius:14px;
#             padding:1.5rem; margin-bottom:1.5rem; color:#8b949e; font-size:0.9rem;">
#   <p style="color:#e6edf3; font-weight:600; margin-bottom:0.6rem;">👋 Hey! I'm NoumanBot</p>
#   <p>I'm your personal AI assistant. Ask me anything about Nouman Ashraf's background, skills, projects, education, or any topic from the loaded knowledge base.</p>
#   <p style="margin-top:0.8rem; margin-bottom:0.4rem;"><b style="color:#a78bfa;">Try asking:</b></p>
#   <ul style="margin:0; padding-left:1.2rem;">
#     <li>What are Nouman Ashraf's technical skills?</li>
#     <li>Tell me about the NLP semester project</li>
#     <li>What projects has he built?</li>
#     <li>What are his career goals?</li>
#   </ul>
# </div>
# """, unsafe_allow_html=True)


# # ── Render chat history ─────────────────────────────────────────────────────
# def render_messages():
#     for msg in st.session_state.messages:
#         role    = msg["role"]
#         content = msg["content"]
#         ts      = msg.get("time", "")
#         sources = msg.get("sources", [])
#         avatar  = "🤖" if role == "assistant" else "👤"
#         bubble_cls = "bot" if role == "assistant" else "user"
#         row_cls    = "user" if role == "user" else ""

#         src_html = ""
#         if sources and role == "assistant":
#             for s in sources[:2]:
#                 src_html += f'<span class="sources-tag">📄 {Path(s).name}</span> '

#         st.markdown(f"""
# <div class="msg-row {row_cls}">
#   <div class="avatar {bubble_cls}">{avatar}</div>
#   <div class="bubble {bubble_cls}">
#     {content}
#     {src_html}
#     <div class="timestamp">{ts}</div>
#   </div>
# </div>
# """, unsafe_allow_html=True)

# render_messages()


# # ── Input area ──────────────────────────────────────────────────────────────
# st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

# col_input, col_btn = st.columns([5, 1])
# with col_input:
#     user_input = st.text_input(
#         label="message",
#         label_visibility="collapsed",
#         placeholder="Ask me anything about Nouman Ashraf…",
#         key="chat_input",
#     )
# with col_btn:
#     send = st.button("Send ➤", use_container_width=True)


# # ── Handle submission ────────────────────────────────────────────────────────
# def handle_query(question: str):
#     if not question.strip():
#         return
#     if not st.session_state.ready:
#         st.warning("⚠️ Please initialize NoumanBot first using the sidebar.")
#         return

#     ts = time.strftime("%H:%M")

#     # Add user message
#     st.session_state.messages.append({
#         "role": "user", "content": question, "time": ts, "sources": []
#     })

#     with st.spinner("NoumanBot is thinking…"):
#         try:
#             from rag_pipeline import query_rag
#             result = query_rag(st.session_state.chain, question)
#             answer  = result["answer"]
#             sources = result["sources"]
#             st.session_state.total_queries += 1
#         except Exception as e:
#             answer  = f"⚠️ An error occurred: {e}"
#             sources = []

#     st.session_state.messages.append({
#         "role": "assistant", "content": answer, "time": ts, "sources": sources
#     })
#     st.rerun()


# if send and user_input:
#     handle_query(user_input)
# elif user_input and user_input.endswith("\n"):   # Enter key fallback
#     handle_query(user_input.strip())

# # ── Quick-suggest chips ──────────────────────────────────────────────────────
# if not st.session_state.messages:
#     st.markdown("<div style='margin-top:0.5rem; color:#8b949e; font-size:0.8rem;'>Quick questions:</div>", unsafe_allow_html=True)
#     q_cols = st.columns(4)
#     chips = [
#         "What are his skills?",
#         "Tell me about NoumanBot project",
#         "What's his CGPA?",
#         "List his certifications",
#     ]
#     for i, chip in enumerate(chips):
#         with q_cols[i]:
#             if st.button(chip, key=f"chip_{i}", use_container_width=True):
#                 handle_query(chip)


"""
app.py  –  NoumanBot: Personal RAG Chatbot
Glassmorphism UI with auto-clearing input
"""

import warnings, logging
warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.ERROR)

import os, time
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="NoumanBot – Personal AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: #0a0a1a !important;
    color: #e8e8f0 !important;
}

/* animated mesh background */
body::before {
    content: '';
    position: fixed; inset: 0; z-index: -1;
    background:
        radial-gradient(ellipse 80% 60% at 20% 10%, rgba(99,102,241,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 80% 80%, rgba(168,85,247,0.15) 0%, transparent 60%),
        radial-gradient(ellipse 50% 40% at 60% 30%, rgba(14,165,233,0.10) 0%, transparent 55%),
        #0a0a1a;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header, .stDeployButton { display: none !important; }
.block-container { padding: 1.5rem 2rem 4rem !important; max-width: 960px; margin: 0 auto; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(15,15,30,0.85) !important;
    backdrop-filter: blur(20px) !important;
    border-right: 1px solid rgba(255,255,255,0.07) !important;
}

/* ── Glass card mixin ── */
.glass {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 20px;
}

/* ── Header ── */
.header-wrap {
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(30px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.header-wrap::before {
    content: '';
    position: absolute; top: -40%; left: -10%;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(99,102,241,0.25) 0%, transparent 70%);
    pointer-events: none;
}
.header-wrap::after {
    content: '';
    position: absolute; bottom: -30%; right: 5%;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(168,85,247,0.20) 0%, transparent 70%);
    pointer-events: none;
}
.header-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a5b4fc 0%, #c084fc 50%, #67e8f9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
}
.header-sub { color: rgba(255,255,255,0.45); font-size: 0.9rem; margin-top: 6px; }
.status-pill {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.75rem;
    color: rgba(255,255,255,0.5);
    margin-top: 12px;
}
.status-pill.online { color: #86efac; border-color: rgba(134,239,172,0.25); background: rgba(134,239,172,0.07); }
.dot { width:7px; height:7px; border-radius:50%; background:#86efac; animation: blink 2s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* ── Welcome card ── */
.welcome-card {
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1.2rem;
    color: rgba(255,255,255,0.5);
    font-size: 0.88rem;
    line-height: 1.7;
}
.welcome-card strong { color: rgba(255,255,255,0.85); }
.welcome-card .chip-row { margin-top: 12px; display: flex; flex-wrap: wrap; gap: 8px; }
.welcome-card .chip {
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.78rem;
    color: #a5b4fc;
}

/* ── Chat messages ── */
.msg-row {
    display: flex;
    gap: 12px;
    align-items: flex-start;
    margin-bottom: 1rem;
    animation: fadeUp 0.3s ease;
}
@keyframes fadeUp { from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:translateY(0)} }
.msg-row.user { flex-direction: row-reverse; }

.avatar {
    width: 36px; height: 36px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem; flex-shrink: 0;
    border: 1px solid rgba(255,255,255,0.10);
}
.avatar.bot  { background: linear-gradient(135deg, rgba(99,102,241,0.5), rgba(168,85,247,0.5)); }
.avatar.user { background: linear-gradient(135deg, rgba(14,165,233,0.5), rgba(6,182,212,0.4)); }

.bubble {
    max-width: 72%;
    padding: 0.9rem 1.15rem;
    border-radius: 18px;
    font-size: 0.9rem;
    line-height: 1.65;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
}
.bubble.bot {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.09);
    border-top-left-radius: 4px;
    color: #dde1f0;
}
.bubble.user {
    background: rgba(99,102,241,0.18);
    border: 1px solid rgba(99,102,241,0.28);
    border-top-right-radius: 4px;
    color: #e0e4ff;
}
.bubble .ts {
    font-size: 0.7rem;
    color: rgba(255,255,255,0.25);
    margin-top: 6px;
    display: block;
}
.src-tag {
    display: inline-block;
    font-size: 0.7rem;
    background: rgba(168,85,247,0.12);
    color: #c084fc;
    border: 1px solid rgba(168,85,247,0.22);
    border-radius: 4px;
    padding: 1px 7px;
    margin-top: 6px;
    margin-right: 4px;
}

/* ── Input ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 14px !important;
    color: #e8e8f0 !important;
    padding: 0.8rem 1.1rem !important;
    font-size: 0.92rem !important;
    font-family: 'Inter', sans-serif !important;
    transition: border-color 0.25s, box-shadow 0.25s !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(99,102,241,0.55) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12), 0 0 20px rgba(99,102,241,0.08) !important;
    outline: none !important;
}
.stTextInput > div > div > input::placeholder { color: rgba(255,255,255,0.25) !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, rgba(99,102,241,0.7), rgba(168,85,247,0.65)) !important;
    backdrop-filter: blur(10px) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 12px !important;
    padding: 0.65rem 1.2rem !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.2s !important;
    width: 100% !important;
    letter-spacing: 0.01em !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, rgba(99,102,241,0.9), rgba(168,85,247,0.85)) !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.3) !important;
    transform: translateY(-1px) !important;
    border-color: rgba(255,255,255,0.22) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Stat cards ── */
.stat-card {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1rem;
    text-align: center;
}
.stat-card .val {
    font-family: 'Syne', sans-serif;
    font-size: 1.7rem; font-weight: 800;
    background: linear-gradient(135deg, #a5b4fc, #c084fc);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.stat-card .lbl { font-size: 0.72rem; color: rgba(255,255,255,0.35); margin-top: 3px; }

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.07) !important; margin: 1rem 0 !important; }

/* ── Sidebar text ── */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown { color: rgba(255,255,255,0.5) !important; font-size: 0.83rem; }

/* ── Alerts ── */
.stAlert { background: rgba(255,255,255,0.04) !important; border-radius: 12px !important; backdrop-filter: blur(10px) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.10); border-radius: 4px; }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1.5px dashed rgba(255,255,255,0.12) !important;
    border-radius: 14px !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: #a5b4fc !important; }
</style>
""", unsafe_allow_html=True)


# ── Cache RAG init ────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def init_rag(api_key: str):
    from rag_pipeline import get_retriever, build_rag_chain
    retriever = get_retriever()
    chain     = build_rag_chain(retriever, api_key)
    return chain


# ── Session state ─────────────────────────────────────────────────────────
def init_state():
    for k, v in {
        "messages": [], "chain": None, "ready": False,
        "total_queries": 0, "input_key": 0,
    }.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ── SIDEBAR ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    st.markdown("---")

    api_key = st.text_input(
        "🔑 Groq API Key",
        type="password",
        value=os.getenv("GROQ_API_KEY", ""),
        placeholder="gsk_...",
        help="Get your free key at console.groq.com",
    )

    st.markdown("### 📂 Add Documents")
    uploaded = st.file_uploader(
        "Upload .txt or .pdf files",
        accept_multiple_files=True,
        type=["txt", "pdf"],
    )
    if uploaded:
        Path("data").mkdir(exist_ok=True)
        for f in uploaded:
            (Path("data") / f.name).write_bytes(f.read())
        st.success(f"✅ {len(uploaded)} file(s) added")
        init_rag.clear()
        st.session_state.chain = None
        st.session_state.ready = False

    st.markdown("---")

    if st.button("🚀 Initialize NoumanBot", use_container_width=True):
        if not api_key:
            st.error("Please enter your Groq API key first.")
        else:
            with st.spinner("Building knowledge base…"):
                try:
                    st.session_state.chain = init_rag(api_key)
                    st.session_state.ready = True
                    st.success("NoumanBot is ready!")
                except Exception as e:
                    st.error(f"Error: {e}")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.total_queries = 0
        st.rerun()

    st.markdown("---")
    st.markdown("### 📊 Session")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="stat-card"><div class="val">{st.session_state.total_queries}</div><div class="lbl">Queries</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-card"><div class="val">{len(st.session_state.messages)}</div><div class="lbl">Messages</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""<div style="font-size:0.76rem;color:rgba(255,255,255,0.3);line-height:1.8;">
<b style="color:rgba(255,255,255,0.5)">NoumanBot</b> · NLP Project CC438<br>
UMT Lahore · Spring 2026<br><br>
LangChain · BM25 · Groq LLaMA 3.1 · Streamlit
</div>""", unsafe_allow_html=True)


# ── MAIN ─────────────────────────────────────────────────────────────────

# Header
status_cls  = "online" if st.session_state.ready else ""
status_text = '<span class="dot"></span>Online' if st.session_state.ready else "⏸ Not initialized"
st.markdown(f"""
<div class="header-wrap">
  <div class="header-title">🤖 NoumanBot</div>
  <div class="header-sub">Personal AI Assistant · Nouman Ashraf · UMT Lahore</div>
  <div class="status-pill {status_cls}">{status_text}</div>
</div>
""", unsafe_allow_html=True)

# Welcome (empty chat)
if not st.session_state.messages:
    st.markdown("""
<div class="welcome-card">
  <strong>👋 Hey! I'm NoumanBot</strong><br>
  I'm Nouman Ashraf's personal AI assistant. Ask me anything about his background, skills, projects, or education.
  <div class="chip-row">
    <span class="chip">What are his skills?</span>
    <span class="chip">Tell me about his projects</span>
    <span class="chip">What's his CGPA?</span>
    <span class="chip">NLP project details</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Render messages
for msg in st.session_state.messages:
    role      = msg["role"]
    content   = msg["content"]
    ts        = msg.get("time", "")
    sources   = msg.get("sources", [])
    avatar    = "🤖" if role == "assistant" else "👤"
    bub_cls   = "bot" if role == "assistant" else "user"
    row_cls   = "user" if role == "user" else ""

    src_html = ""
    if sources and role == "assistant":
        for s in sources[:2]:
            src_html += f'<span class="src-tag">📄 {Path(s).name}</span>'

    st.markdown(f"""
<div class="msg-row {row_cls}">
  <div class="avatar {bub_cls}">{avatar}</div>
  <div class="bubble {bub_cls}">
    {content}
    {src_html}
    <span class="ts">{ts}</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Input area (key trick clears the box after send) ─────────────────────
st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
col_input, col_btn = st.columns([5, 1])

with col_input:
    user_input = st.text_input(
        label="msg",
        label_visibility="collapsed",
        placeholder="Ask me anything about Nouman Ashraf…",
        key=f"chat_input_{st.session_state.input_key}",
    )
with col_btn:
    send = st.button("Send ➤", use_container_width=True)

# Quick chips (only when empty)
if not st.session_state.messages:
    chips = ["What are his skills?", "List his projects", "What's his CGPA?", "Certifications?"]
    cols  = st.columns(4)
    for i, chip in enumerate(chips):
        with cols[i]:
            if st.button(chip, key=f"chip_{i}", use_container_width=True):
                user_input = chip
                send = True


# ── Handle send ───────────────────────────────────────────────────────────
def handle_query(question: str):
    if not question.strip():
        return
    if not st.session_state.ready:
        st.warning("⚠️ Please initialize NoumanBot first using the sidebar.")
        return

    ts = time.strftime("%H:%M")
    st.session_state.messages.append({"role": "user", "content": question, "time": ts, "sources": []})

    with st.spinner("NoumanBot is thinking…"):
        try:
            from rag_pipeline import query_rag
            result  = query_rag(st.session_state.chain, question)
            answer  = result["answer"]
            sources = result["sources"]
            st.session_state.total_queries += 1
        except Exception as e:
            answer  = f"⚠️ Error: {e}"
            sources = []

    st.session_state.messages.append({"role": "assistant", "content": answer, "time": ts, "sources": sources})
    # Bump key → Streamlit creates a brand-new input widget (clears the box)
    st.session_state.input_key += 1
    st.rerun()


if send and user_input:
    handle_query(user_input)