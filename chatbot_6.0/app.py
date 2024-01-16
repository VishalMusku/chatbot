import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import pdf_to_docx_convertor
import context_generator
import time
import tempfile

load_dotenv()

key=os.getenv("GOOGLE_API_KEY")

def get_pdf_text():
    txt_file_path = 'output_combined.txt'
    
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        text=file.read()
    
    return text

def save_uploaded_file(uploaded_file):
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    
    # Save the uploaded file to the temporary directory
    file_path = os.path.join(temp_dir,uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())
    
    return file_path

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

 
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")


def get_conversational_chain():

    prompt_template = """ Answer the question below using the provided context only and no external knowledge. The context involves tabular data in pipe separated string format so carefully extract the proper information while reading the tables. \n\n
                        Context: \n {context}?\n
                        Question: \n {question} \n
                        Answer:
                    """

    model = ChatGoogleGenerativeAI(model="gemini-pro",google_api_key=key)

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain



def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    
    new_db = FAISS.load_local("faiss_index", embeddings)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    
    response = chain(
        {"input_documents":docs, "question": user_question}
        , return_only_outputs=True)

    print(response['output_text'])
    
    
    st.write("Answer : ", response["output_text"])


def main():
    st.set_page_config("Chat PDF")
    st.header("Chat with PDF :")

    user_question = st.text_input("Ask a Question :")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu:")
        uploaded_file = st.file_uploader("Upload your PDF File", accept_multiple_files=False)
        if st.button("Submit"):
            with st.spinner("Processing..."):
                save_uploaded_file(uploaded_file)
                time.sleep(10)
                context_generator.main()
                raw_text = get_pdf_text()
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")
                

def save_uploaded_file(uploaded_file):
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    
    # Save the uploaded file to the temporary directory
    file_path = os.path.join(temp_dir,uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())
    
    pdf_to_docx_convertor.pdf_to_docx(file_path) 




if __name__ == "__main__": 
    load_dotenv()
    key=os.getenv("GOOGLE_API_KEY")
    main()
    



