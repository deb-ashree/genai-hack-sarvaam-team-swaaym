import json
import os
from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI
import requests, re
import streamlit as st
from streamlit_mic_recorder import speech_to_text 
from gtts import gTTS
import playsound
from dotenv import load_dotenv
# import speech_recognition as sr
import google.generativeai as genai
from langchain_community.document_loaders import PyPDFLoader

from tools.AudioTools import createAudioWithSarvaamBulbulV1
from utility.document_loader import LoadContextData

from data_models.user_input_object import UserInput
from typing_extensions import List
from pydantic import BaseModel, Field, HttpUrl

load_dotenv(os.getcwd()+"/local.env")   
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

if not os.path.exists('speech'):
    os.makedirs('speech')

def sarvamASRTranslate():
    ## Using sarvam's saras model
    url = "https://api.sarvam.ai/speech-to-text-translate"
    payload = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"prompt\"\r\n\r\n<string>\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"model\"\r\n\r\nsaaras:v1\r\n-----011000010111000001101001--\r\n\r\n"
    headers = {"Content-Type": "multipart/form-data", "boundary":"----WebKitFormBoundary7MA4YWxkTrZu0gW", "api-subscription-key":"ec17625a-c39a-46da-a075-7dd41cd75052"}

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)

def callModel(prompt):
    ## Using Gemini
    # model = ChatGoogleGenerativeAI(model="gemini-1.5-pro",
    #         google_api_key=os.environ['GEMINI_API_KEY'],
    #         verbose = True,
    # )
    # result = model.invoke(prompt)
    # response = result.content

    genai.configure(api_key = os.environ['GEMINI_API_KEY'])
    model = genai.GenerativeModel('gemini-1.5-flash')  #,generation_config={"response_mime_type": "application/json"})  
    result = model.generate_content(  prompt,
                                        generation_config=genai.GenerationConfig(response_mime_type="application/json",
                                        response_schema = UserInput))
    response = result.text

    return response

def speak(text, language):
    tts = gTTS(text=text, lang="en")
    print(language)
    filename = "speech/speaker_audio.mp3"
    tts.save(filename)

    ## Sarvam needs a fix
    # tts = createAudioWithSarvaamBulbulV1(text, language, filename, "female")

    playsound.playsound(filename)

def generate_response(transcript, instruction_prompt, language):
    
    print(f"\nUser: {transcript}")
    ## Call model
    
    response = callModel(transcript+instruction_prompt)

    print(f" Response received : {response}")
    speak("Thank you for your response!",language)
    
    #getaudio()

    print(f"\nResponse transcription: ", end="\r\n")
    return response

class ASRHome():
    def app(self):
        language = st.selectbox("Select Language", ["English","Hindi","Kannada", "Marathi"])
        mic_text_input = speech_to_text(
                            language='en',
                            start_prompt="🎤",
                            stop_prompt="❏",
                            just_once=False,
                            use_container_width=False,
                            callback=None,
                            args=(),
                            kwargs={},
                            key=None
                        )
        # var = ""
        ##  Prompt Collection
        prompt = """
                                Hello Welcome, how can I assist you today? Please share more about the topic you want to generate content in, with the following details:
                                1. Class For which content is to be generated
                                2. Subject for the topic
                                3. Topic for course
                """

                            # 1. Class For which content is to be generated
                            # 2. Subject for the topic
                            # 3. Topic for course
                            # 4. Language basis the language spoken in

        postscript = f""" Create and return a json response only in the format :
                            
                                "Class": <class mentioned in user input>,
                                "Subject": <subject mentioned in user input>,
                                "Topic": <topic mentioned in user input>,
                                "Language": <the language of the user input>
                        
                        """
        # subpostscript = f""" You are a course creation assistant. Please summarize the response basis what the user said then create and return a json response only in the format :
                            
        #                         "{var}": <as mentioned in user input>
                        
        #                 """
        subpostscript = f""" You are a course creation assistant.Please check the response basis what the user said  return 1-2 words answer only"""

        ## Uploading of relevant documents
        uploaded_file = st.file_uploader("Please upload a PPDF File or a PDF Textbook for reference in course content generation ", type=["pdf"])
            
        if st.session_state["isStart"] == 0:
            speak(prompt, language)
            st.session_state["isStart"] = 1        

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
                
        if mic_text_input is not None:
            print(f"Input received {mic_text_input}")
            # var = ""
            # guided_prompt = f"Please provide details about "

            # if json_response["Class"] is None:
            # var = "Class"
            # print(guided_prompt)
            res = generate_response(mic_text_input,postscript, language)
            print(f"Received response : {res}")
            json_response = json.loads(res)
            grade = json_response["grade"]
            print(grade)
            subject = json_response["subject"]
            print(subject)
            topic = json_response["topic"]
            print(topic)
            language = language
            print(language)

            input = UserInput(grade=grade, subject=subject, topic=topic, language=language, instructions=" ", review_status="pending")
            print(f"Input details : {input}")
            return input.model_dump(mode='json')
        
# if __name__ == "__main__":
#     sarvamASRTranslate()



