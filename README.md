# Multimodal PDF RAG & Agentic RAG Experiments

This repository is a collection of hands-on projects where I experimented with different architectures of **RAG (Retrieval-Augmented Generation)** using LangChain (v0.3), Groq Cloud (Llama/Qwen), and local Hugging Face Embeddings. 

The project tracks my journey from building a classic, simple PDF Q&A setup to modern **LCEL (LangChain Expression Language) Pipelines** and fully autonomous **ReAct-style AI Agents**.

---

## 🚀 What's Inside? (The 3 Projects)

I have structured this repository into three distinct architectural implementations:

### 1. Multi-PDF Chat Application with Custom UI (`app_v1.py`)
A production-ready full-stack chat interface capable of ingestion and reasoning over multiple PDF files simultaneously.
* **UI/UX:** Streamlit backend rendered with custom, elegant HTML/CSS chat bubbles for a professional look.
* **Core Framework:** Built using LangChain v0.3's modern **LCEL pipeline (`|`)**, completely avoiding deprecated or messy legacy chain imports.
* **State Management:** Uses formal `HumanMessage` and `AIMessage` objects inside Streamlit's session state to maintain accurate conversation context across multiple turns.
* **Models:** Powered by `llama-3.3-70b-versatile` via Groq for high-speed generation, and local `all-MiniLM-L6-v2` embeddings.

### 2. Autonomous Agentic RAG (`agent.py`)
Moving beyond standard text retrieval, this script implements an **AI Agent** that actively decides how and when to look for information.
* **Reasoning Engine:** Utilizes the advanced `qwen3-32b` model with a native reasoning format parser.
* **Tool-Driven Execution:** Uses a custom LangChain `@tool` (`retrieve_context`). The agent evaluates the user query and autonomously invokes this tool if it needs document data.
* **Live Streaming:** Streams the agent's actual internal "thinking process" and tool execution logs directly to the terminal live.
* **Storage:** Leverages a lightweight `InMemoryVectorStore` to hold embeddings directly in RAM for instant lookups.

### 3. Classic Single-PDF Q&A System (`app_classic.py`)
The baseline/traditional implementation of RAG included for comparative analysis.
* **Framework:** Utilizes the legacy `load_qa_chain` ("stuff" type format) approach.
* **Models:** Uses `llama-3.1-8b-instant` via Groq. It’s a great lightweight reference script for spinning up a quick single-document QA pipeline.

---

## 🛠️ Tech Stack

* **Orchestration:** LangChain (v0.3), LangChain Core, LangChain Community
* **LLM Providers:** Groq Cloud Ecosystem (`llama-3.3-70b`, `llama-3.1-8b`, `qwen-32b`)
* **Embeddings:** Hugging Face (`sentence-transformers/all-MiniLM-L6-v2` — 100% free and runs locally)
* **Vector Databases:** FAISS (Facebook AI Similarity Search) & InMemoryVectorStore
* **Frontend UI:** Streamlit 
* **PDF Parsing:** PyPDF2 & PyMuPDF (Fitz)

---

## 📦 Installation & Setup

1. Clone the repository and initialize a Virtual Environment

git clone <your-repository-link>
cd pdf-rag-agent-langchain
python -m venv venv
# Activate virtual environment
venv\Scripts\activate          # On Windows

2. Install dependencies

pip install streamlit langchain langchain-groq langchain-huggingface langchain-community

3. Setup your Environment Variables
Create a .env file in the root directory of your project and paste your Groq API key:

GROQ_API_KEY=gsk_your_actual_groq_api_key_here