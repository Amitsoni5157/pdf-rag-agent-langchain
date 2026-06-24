from dotenv import load_dotenv
import streamlit as st
import os
from pypdf import PdfReader

from langchain_text_splitters import CharacterTextSplitter
# from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_groq import ChatGroq
from langchain_classic.chains.question_answering import load_qa_chain
# from langchain_openai import OpenAI
# from langchain_community.callbacks.manager import get_openai_callback

def main():
    load_dotenv()

    api_key = os.getenv("GROQ_API_KEY")

    st.set_page_config(page_title="Ask your PDF")
    st.header("Ask your PDF")

    #  Upload the file
    pdf = st.file_uploader("Upload your PDF", type="pdf")
    
    if pdf is None:
        st.info("Please upload a PDF.")
        return
    
    # Extract the text
    text = ""
    # if pdf is not None:
    pdf_reader = PdfReader(pdf)
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    # Split into chunks
    text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
    )
    chunks = text_splitter.split_text(text)

    # st.write(chunks)

    # create embedings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    knowledge_base = FAISS.from_texts(chunks, embeddings)

    # show user input
    user_question = st.text_input("Ask a question about your PDF:")

    if user_question:
        docs = knowledge_base.similarity_search(user_question)

        # llm = OpenAI()
        llm = ChatGroq(
                api_key=api_key,
                model="llama-3.1-8b-instant"
            )
        
        chain = load_qa_chain(llm, chain_type="stuff")

        response = chain.run(
            input_documents=docs,
            question=user_question

            )
            

        st.write(response)



if __name__ == '__main__':
    main()