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
import docx_to_text
import time
import tempfile
import context_generator
from pathlib import Path
import pdf2text

load_dotenv()

key=os.getenv("GOOGLE_API_KEY")

def get_pdf_text(path_):
    txt_file_path = path_
    
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        text=file.read()
    
    return text


def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

 
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")


def get_conversational_chain():

    prompt_template = """ Answer the question below correctly from the context provided below.  \n\n
                          
                          
                          context : \n {context} \n
                          
                          
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


    
    response=response['output_text']
    
    final_response=f"Response : {response}"
    

    txt=''
    
    for i in range(0,len(docs)):
        txt+=docs[i].page_content
    
    with open('context.txt','w') as f:
        f.write(txt)
    
    st.write(final_response)

    print(txt)

def main():
    st.set_page_config("PDF search chatbot")
    
    st.header("Chat with your PDF :")

    user_question = st.text_input("Ask a Question here :")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu:")
        uploaded_file = st.file_uploader("Upload your PDF File", accept_multiple_files=False)
        if st.button("Submit"):
            with st.spinner("Processing..."):
                
                base_name_ = Path(os.path.basename(uploaded_file.name)).stem
                
                base_name=base_name_+'.txt'

                pdf2text.extract_text_save_to_file(save_uploaded_file(uploaded_file), "{}".format(base_name))

                raw_text = get_pdf_text('{}'.format(base_name))
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
    
    return file_path


if __name__ == "__main__": 
    load_dotenv()
    key=os.getenv("GOOGLE_API_KEY")
    main()
    







