# pip install langchain langchainhub langchain_community

from pathlib import Path
import sys
import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from langchain_openai import ChatOpenAI
# from langchain_ollama import ChatOllama
from langchain.chains import RetrievalQA
from langchain import hub
import traceback, logging
import pprint
from os import listdir
from os.path import isfile, join
from utility.pdf_ocr_to_text_with_fitz import ScannedDataExtractor

load_dotenv(os.getcwd()+"/local.env")
os.environ['OPENAI_API_KEY']=os.getenv("OPENAI_API_KEY")
os.environ['USER_AGENT'] = 'test_agent'

ef_openai = OpenAIEmbeddings()

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

class LoadContextData():
    def __init__(self):
        self.llm_gpt = ChatOpenAI(model="gpt-4o-mini") ## Calling Gpt-4o 
        self.prompt = "You are a helpful assistant who gets the available information from the context given. Only provide answer from the current context provided. Otherwise you can mention that you are capable to answer only basis the data provided"  #hub.pull("rlm/rag-prompt")
        # logging.debug(self.prompt)
        # self.llm_ollama = ChatOllama(
        #     model="llama3.1",
        #     temperature=.7,
        # )
        self.ef_openai = OpenAIEmbeddings()
        self.vector = Chroma(persist_directory="chromaDB", embedding_function=self.ef_openai, collection_name="test_chroma_db")

    def loadAndStoreFiles(self, type):
        logging.debug("Loading data")
        # load from disk
        self.vector = Chroma(persist_directory="chromaDB", embedding_function=self.ef_openai, collection_name="test_chroma_db")
        logging.debug("Creating Vector")
        text_splitter = RecursiveCharacterTextSplitter(
                        chunk_size=1500,
                        chunk_overlap=200,
                        length_function=len )
        
        # 1. Load Data from The Web

        if type == "web":
            print(f" Type is : {type}")
        # Get a Web Data Loader

        # List of URLs to load the documents from
            urls = [
            #     # "https://www.careerguidancejpgandhi.com/",
            #     # "https://www.mindler.com/blog/medical-courses-after-12th/",
            #     # "https://www.joinindiannavy.gov.in/en/page/medical.html",
            #     # "https://www.shiksha.com/engineering-career-chp",
            #     "https://www.careers360.com",
            #     "https://collegedunia.com/",
            #     # "https://gettinggrowth.com/career-in-marketing/",
            #     # "https://edufever.in/career-in-journalism-in-india/#:~:text=to%20achieve%20this.-,Job%20Opportunities%20for%20Journalism,a%20degree%20in%20broadcast%20journalism.",
            #     # "https://edufever.in/category/courses/",
                    "https://maharashtracareerportal.com/#googtrans(en)",
            ]
            # Load documents from the URLs
            docs = [WebBaseLoader(url).load() for url in urls]
            docs_list = [item for sublist in docs for item in sublist]

            documents = text_splitter.split_documents(docs_list)
            documents

            # Convert data to Vector Database

            # persist to disk
            self.vector = Chroma.from_documents(collection_name="test_chroma_db", documents=documents, 
                                        embedding=self.ef_openai, persist_directory='chromaDB') 
            logging.debug(self.vector)

            # ****** for a single pdf ************

            # logging.debug("Loading from the Web")
            # loader = WebBaseLoader("https://docs.smith.langchain.com/user_guide")
            # data = loader.load()
            # data
            # documents = text_splitter.split_documents(data)
            # documents

            # ****** for a single pdf ************

        # 2. Load Data from the PDFs
        if type == "pdf":
            print(f" Type is : {type}")
            logging.debug("Loading from the PDF")
            path_to_pdfs = 'pdf_files/'
            pdf_splits = []
            if os.path.exists(path_to_pdfs):
                logging.debug("Steps ++++\n1..")
                file_list = os.listdir(path_to_pdfs)
                if len(file_list) > 0:
                    logging.debug("2..")
                    for file in file_list:
                        logging.debug("3..")
                        file = os.path.join(path_to_pdfs,file)
                        logging.debug(file)
                        loader = PyPDFLoader(file)
                        data = loader.load()
                        logging.debug("4..")
                        pdf_splits.extend(text_splitter.split_documents(data))

            # Convert data to Vector Database
            if pdf_splits is not []:
                self.vector.from_documents(collection_name="test_chroma_db", documents=pdf_splits, 
                                    embedding=self.ef_openai, persist_directory='chromaDB')  #(pdf_splits,embedding=self.ef_openai)
            logging.debug(self.vector)

        # # 3. Load Data from Images and Scanned Text
        # path_to_scans = 'scanned_pdf_files/'
        # output_path = 'scanned_pdf_files/scans/'
        # file_prefix = "image"
        # file_list = os.listdir(path_to_scans)
        # # scannedText = ""
        # if len(file_list) > 0:
        #     print(len(file_list))
        #     extractor = ScannedDataExtractor()
        #     scannedText = extractor.extractImagesWithFitz(file_list, output_path, path_to_scans)
        #     print(f" Check scans : {scannedText}")
        #     # scan_text_extract = [[extractor.readScan(output_path+item) for item in listdir(output_path) if isfile(join(output_path, item))]]
        #     extractor.cleanUpImages(output_path)
        #     if scannedText:
        #         scannedText = scannedText.replace('"',"").replace("'/","")
        #         print("Cleaned text scan ")
        #         print(scannedText)
        #         text_splitter = RecursiveCharacterTextSplitter(
        #             chunk_size=1500,
        #             chunk_overlap=200,
        #             length_function=len
        #         )
        #         scan_splits = text_splitter.split_text(scannedText)

        #         self.vector.add_texts(
        #                 texts = scan_splits,
        #                 embedding = self.ef_openai,
        #                 collection_name="test_chroma_db", 
        #                 persist_directory='chromaDB'
        #             )

        return self.vector

    # Make a RAG pipeline
    def getVector(self):
        return self.vector
    
    def getEmbeddingFunc(self):
        return self.ef_openai
    
    def queryDataFromVector(self,vector, query, language):
        logging.debug("Creating chain")
        logging.debug(vector)
        qa_chain = RetrievalQA.from_chain_type(
                self.llm_gpt,
                retriever=vector.as_retriever(),
                #chain_type_kwargs={"prompt": self.prompt}
            )
        #question = "How is Langchain used. Respond in proper Marathi without any unicode characters" # "WHat is a Data Mesh and how is it created" "Explain Monitoring and A/B Testing in langsmith", "Who is a casual taxable person
        result = qa_chain.invoke({"query": f" {query}. Respond in the language of the query or the preferred {language} and use that language based script" + self.prompt })
        # logging.debug(result)

        import pprint
        pp = pprint.PrettyPrinter(indent=5)
        pp.pprint(result["result"])
        return result