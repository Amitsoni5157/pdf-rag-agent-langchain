import streamlit as st
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader

from langchain_groq import ChatGroq

# LangChain v0.3 Updated Imports
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS

from langchain_huggingface import HuggingFaceEmbeddings

# LCEL Pipeline Imports
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

# HTML Templates for custom chat UI
from htmlTemplates import css, bot_template, user_template
from operator import itemgetter
from langchain_core.messages import HumanMessage, AIMessage


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text
    
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks
    

def get_vectorstore(text_chunks):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        api_key=os.getenv("GROQ_API_KEY")
    )
   
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Use the following context to answer the question accurately:\n\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])

    #  step 1: format docs function
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    #  step 2: LCEL retrieval chain (REPLACEMENT)
    conversation_chain = (
        {
            "context": itemgetter("input") | retriever | format_docs,
            "input": lambda x: x["input"],
            "chat_history": lambda x: x["chat_history"]
        }
        | qa_prompt
        | llm
        | StrOutputParser()
    )

    return conversation_chain

def handle_userinput(user_question):
    if st.session_state.conversation is None:
        st.warning("Please upload and process your PDFs first !")
        return
    
    with st.spinner('Thinking....'):
        response = st.session_state.conversation.invoke({
            "input":user_question,
            "chat_history":st.session_state.chat_history
        })
        st.session_state.chat_history.append(HumanMessage(content=user_question))
        st.session_state.chat_history.append(AIMessage(content=response))

        for message in st.session_state.chat_history:
            if isinstance(message, HumanMessage):
                st.write(
                    user_template.replace("{{MSG}}", message.content),
                    unsafe_allow_html=True
            )
            elif isinstance(message, AIMessage):
                st.write(
                    bot_template.replace("{{MSG}}", message.content),
                    unsafe_allow_html=True
                )

def main():
    load_dotenv()
    
    # Validation to check if HuggingFace Token exists
    if not os.getenv("GROQ_API_KEY"):
        st.error("GROQ_API_KEY is not set in your .env file!")
        st.stop()

    st.set_page_config(page_title="Chat with multiple Pdfs", page_icon=":book:")
    st.write(css, unsafe_allow_html=True)

    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.header("Chat with multiple Pdf's :books:")
    
    user_question = st.text_input("Ask a question about your documents:")
    
    if user_question:
            handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your Documents")
        pdf_docs = st.file_uploader("Upload your Pdf here and click on 'Process'", accept_multiple_files=True)
        
        if st.button("Process"):
            if pdf_docs:
                with st.spinner("Processing..."):                    
                    raw_text = get_pdf_text(pdf_docs)                
                    text_chunks = get_text_chunks(raw_text)                    
                    vectorstore = get_vectorstore(text_chunks)
                    st.session_state.conversation = get_conversation_chain(vectorstore)
                    st.success("Done! You can now ask questions.")
            else:
                st.error("Please upload at least one PDF file!")

if __name__ == '__main__':
    main()