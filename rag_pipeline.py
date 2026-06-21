"""
rag_pipeline.py
RAG system using BM25 retriever (no internet/model download needed)
+ Groq LLaMA 3 for generation
"""

import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.retrievers import BM25Retriever
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

load_dotenv()


# ─────────────────────────────────────────
# 1. Load & preprocess documents
# ─────────────────────────────────────────

def load_documents(data_dir: str = "data") -> list:
    docs = []
    data_path = Path(data_dir)
    for txt_file in data_path.glob("*.txt"):
        try:
            loader = TextLoader(str(txt_file), encoding="utf-8")
            docs.extend(loader.load())
        except Exception as e:
            print(f"Error loading {txt_file}: {e}")
    for pdf_file in data_path.glob("*.pdf"):
        try:
            loader = PyPDFLoader(str(pdf_file))
            docs.extend(loader.load())
        except Exception as e:
            print(f"Error loading {pdf_file}: {e}")
    print(f"Loaded {len(docs)} document(s)")
    return docs


def split_documents(docs: list, chunk_size: int = 500, chunk_overlap: int = 80) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    chunks = splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks")
    return chunks


# ─────────────────────────────────────────
# 2. BM25 Retriever (no internet needed)
# ─────────────────────────────────────────

def build_bm25_retriever(chunks: list, k: int = 4):
    """Build a BM25 keyword retriever — works fully offline."""
    retriever = BM25Retriever.from_documents(chunks)
    retriever.k = k
    print(f"BM25 retriever ready with {len(chunks)} chunks")
    return retriever


def get_retriever(data_dir: str = "data", k: int = 4):
    docs     = load_documents(data_dir)
    chunks   = split_documents(docs)
    retriever = build_bm25_retriever(chunks, k=k)
    return retriever


# ─────────────────────────────────────────
# 3. Prompt Engineering
# ─────────────────────────────────────────

SYSTEM_TEMPLATE = """You are NoumanBot, a friendly and intelligent personal AI assistant.
Use the retrieved context below to answer the user's question accurately and helpfully.
If the answer is not clearly in the context, say so politely but still try to help.
Keep responses concise, warm, and professional. Use bullet points where helpful.

Context from knowledge base:
{context}"""

MESSAGES = [
    SystemMessagePromptTemplate.from_template(SYSTEM_TEMPLATE),
    HumanMessagePromptTemplate.from_template("{question}"),
]
QA_PROMPT = ChatPromptTemplate.from_messages(MESSAGES)

CONDENSE_TEMPLATE = """Given the chat history and the follow-up question, rephrase it as a \
standalone question that captures all necessary context.

Chat History:
{chat_history}

Follow-up Question: {question}
Standalone Question:"""
CONDENSE_PROMPT = PromptTemplate.from_template(CONDENSE_TEMPLATE)


# ─────────────────────────────────────────
# 4. Build RAG Chain
# ─────────────────────────────────────────

def build_rag_chain(retriever, api_key: str):
    llm = ChatGroq(
        groq_api_key=api_key,
        model_name="llama-3.1-8b-instant",
        temperature=0.4,
        max_tokens=1024,
    )

    memory = ConversationBufferWindowMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer",
        k=6,
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": QA_PROMPT},
        condense_question_prompt=CONDENSE_PROMPT,
        return_source_documents=True,
        verbose=False,
    )
    return chain


# ─────────────────────────────────────────
# 5. Query Interface
# ─────────────────────────────────────────

def query_rag(chain, question: str) -> dict:
    result = chain.invoke({"question": question})
    sources = list({
        doc.metadata.get("source", "Personal Knowledge Base")
        for doc in result.get("source_documents", [])
    })
    return {"answer": result["answer"], "sources": sources}
