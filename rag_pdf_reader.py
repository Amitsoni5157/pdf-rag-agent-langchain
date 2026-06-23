
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.tools import tool
from langchain.agents import create_agent

# Load environment variables from the .env file (like the GROQ_API_KEY)
load_dotenv()

model = ChatGroq(model='qwen/qwen3-32b', reasoning_format='parsed')

print("Loading PDF document...")
loader = PyMuPDFLoader('ai.pdf')
docs = loader.load()

# Split the heavy PDF text into smaller chunks of 1000 characters to fit LLM context limits
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
all_splits = text_splitter.split_documents(docs)

print("Building embeddings...")
# Using a lightweight local model to turn text chunks into mathematical vectors
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

# Store vectors in RAM using a temporary In-Memory vector store for fast lookup
vector_store = InMemoryVectorStore.from_documents(all_splits,embeddings)

# The @tool decorator registers this function so the AI agent knows it can execute it when needed
@tool
def retrieve_context(query: str):
    '''Retrievs relevant context from the pdf document based on the query.'''
    # Search the vector store to extract the top 3 most relevant text chunks matching the query
    similar_docs = vector_store.similarity_search(query, k=3)
    data = []
    for doc in similar_docs:
        data.append(f'''
            content: {doc.page_content},
            source: {doc.metadata.get('source', 'unknown')}
        ''')
        # Merge the fetched chunks into a single clean string to feed back into the LLM
    return "\n\n".join(data)
    
prompt= 'You are an agent who retrieves context from pdf doc'
# Bind the model and our custom retrieval tool together to build the agent
agent = create_agent(model, [ retrieve_context ], system_prompt=prompt)
query = 'what is Neural Networks according to the documnt ?'

# Stream the agent's internal thinking process and tool executions to the terminal live
for step in agent.stream({"messages":[
    {
        "role": "user",
        "content": query
    }
]}, stream_mode='values'):
    # Beautifully format and print the final conversation stream blocks
    step['messages'][-1].pretty_print()