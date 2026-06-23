# pdf-rag-agent-langchain

# 🤖 PDF RAG Agent with LangChain & Groq

An intelligent, conversational Retrieval-Augmented Generation (RAG) agent capable of parsing complex PDF documents and answering user queries with high factual accuracy, using **LangChain**, **Groq (Qwen 32B)**, and an **InMemory Vector Store**.

---

## 🏗️ System Architecture & Workflow

Here is how the document processing and question-answering pipeline works under the hood:

```text
┌────────────────────────────────────────────────────────┐
│                   1. Ingestion Phase                   │
└────────────────────────────────────────────────────────┘
          [ Your PDF (ai.pdf) ] 
                     │
                     ▼ (PyMuPDFLoader)
          [ Raw Text Loaded ]
                     │
                     ▼ (RecursiveCharacterTextSplitter: Chunk 1000, Overlap 200)
          [ Document Chunks ]
                     │
                     ▼ (HuggingFaceEmbeddings: all-MiniLM-L6-v2)
          [ Vector Embeddings ]
                     │
                     ▼
          [ InMemory Vector Store ]
                     ▲
                     │ (Similarity Search: k=3)
                     │
┌────────────────────┴───────────────────────────────────┐
│                   2. Execution Phase                   │
└────────────────────────────────────────────────────────┘
          [ User Query: "What is NLP?" ]
                     │
                     ▼
          [ LangGraph Agent Node: model ]
                     │
                     ▼ (Decides to use Tool)
          [ Tool Calling: retrieve_context(query) ]
                     │
                     ▼ (Fetches Top 3 Chunks)
          [ Context Formatted & Returned ]
                     │
                     ▼
          [ ChatGroq LLM (qwen/qwen3-32b) ]
                     │
                     ▼
          [ Factual Response Streamed ]


Orchestration & Framework: LangChain & LangGraph (Agentic Flow)

LLM Provider: Groq Cloud (qwen/qwen3-32b)

Embedding Model: HuggingFace (sentence-transformers/all-MiniLM-L6-v2)

Document Parser: PyMuPDF (via PyMuPDFLoader)

Vector Storage: LangChain InMemoryVectorStore


Getting Started
Follow these step-by-step instructions to set up and run the project locally.

1. Clone the Repository
git clone [https://github.com/YOUR_USERNAME/pdf-rag-agent-langchain.git](https://github.com/YOUR_USERNAME/pdf-rag-agent-langchain.git)
cd pdf-rag-agent-langchain

2. Set Up a Virtual Environment
python -m venv venv
.\venv\Scripts\activate

3. Install Requirements
pip install -r requirements.txt

4. Configure Environment Variables
Create a .env file in the root directory of your project (use the provided .env.example as a guide) and add your Groq API Key:
GROQ_API_KEY=gsk_your_actual_groq_api_key_here

5. Add Your PDF Document
Place the PDF document you want to query into the project root directory and name it ai.pdf (or update the filename directly in rag_pdf_reader.py).

6. Run the Agent
Execute the pipeline script to start querying the agent:

python rag_pdf_reader.py