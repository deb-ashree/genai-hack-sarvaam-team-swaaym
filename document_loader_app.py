import os
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader

from utility.document_loader import LoadContextData


## Streamlit app

uploaded_file = st.file_uploader("Please upload a PDF File or a PDF Textbook for reference in course content generation ", type=["pdf"])

context = LoadContextData()
if not os.path.exists('pdf_files'):
   os.makedirs('pdf_files')

if uploaded_file is not None:
    upload_path = 'pdf_files/'
    file_data = uploaded_file.read()
    f = open(upload_path + uploaded_file.name, 'wb')
    f.write(file_data)
    f.close()
    print("File type - "+uploaded_file.type)
    if uploaded_file.type == 'pdf':
        loader = PyPDFLoader(upload_path + uploaded_file.name)
        context.loadAndStoreFiles(uploaded_file.type)

        language = "english"
        question = "Summarize the content from the pdf file uploaded"   #  "How do I get into Engineering" "How do I get into journalism"
        result = context.queryDataFromVector(context.vector, question, language)
        print(f"Response from Context..{result}")

## For testing
# if __name__ == "__main__":
#     old_stdout = sys.stdout
#     log_file = open("message.log","w")
#     sys.stdout = log_file
    
#     context = LoadContextData()
#     print("Load Data..")
#     vector = context.loadAndStoreFiles()
#     print("Loading Data Done..")
#     language = "english"
#     question = "Who is Firdose Kapadia?  "   #  "How do I get into Engineering" "How do I get into journalism"
#     result = context.queryDataFromVector(context.vector, question, language)
#     print("Response from Context..")

#     sys.stdout = old_stdout
#     log_file.close()

