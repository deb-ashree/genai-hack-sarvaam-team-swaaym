import base64
import json
import time, os

from semantic_text_splitter  import TextSplitter
from moviepy.editor import concatenate_audioclips, AudioFileClip
import requests
from tools.TextTools import getSarvamLanguageCode, translateText
from utility.util_functions import makeDir, getFilePath, getS3FilePath, model_tts, model_stt, client
from langchain_core.tools import tool, BaseTool
from dotenv import load_dotenv

load_dotenv(os.getcwd()+"/local.env")

def get_chunks(text, limit):
    splitter = TextSplitter(limit)
    chunks = splitter.chunks(text)
    return chunks

def concatenate_audio_moviepy(audio_clip_paths, output_path):
    """Concatenates several audio files into one audio file using MoviePy
    and save it to `output_path`. Note that extension (mp3, etc.) must be added to `output_path`"""
    clips = [AudioFileClip(c) for c in audio_clip_paths]
    final_clip = concatenate_audioclips(clips)
    final_clip.write_audiofile(output_path)
    s3AudioFile = getS3FilePath(output_path)
    return s3AudioFile

class WhisperAudioTool(BaseTool):
    name: str = "Text to Audio generation tool"
    description: str = "This tool generates and retrieves the video for a {textContent: str} explanation on a specific topic."

    def _run(self, argument: str) -> str:
        try: 
            print("---------")
            print(argument[0])
            print("---------")
            print(argument[1])

            # return textToAudio(argument[0],"../audio/",argument[1], "female")  #"file1.mp3"
            return  manageTextForSarvaam(argument[0],argument[1], argument[2], "female")
            
        except Exception as E:
            raise Exception(E) from E
        

## ------For Audio Generation---------

import speech_recognition as sr

def textToAudio(text, filePath, fileName, gender):
    if gender == "male":
        voice = "alloy"
    elif gender == "female":
        voice = "nova"
    makeDir(filePath)
    print("File name : "+filePath+fileName)
    audioFile = getFilePath(filePath, fileName)
    print(audioFile)
    with client.audio.speech.with_streaming_response.create(
    model=model_tts,
    voice=voice,
    input=text
    ) as  response:
        response.stream_to_file(audioFile)
    time.sleep(20)
    s3AudioFile = getS3FilePath(audioFile)
    return s3AudioFile

def recordedAudioToText(fileName):
    transcription = client.audio.transcriptions.create(
    model=model_stt, 
    file=open(fileName,"rb"))
    return transcription.text

def getAudio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        
        # wait for a second to let the recognizer
        # adjust the energy threshold based on
        # the surrounding noise level 
        r.adjust_for_ambient_noise(source, duration=0.5)

        audio = r.listen(source)
        #playsound.playsound(audio)
        input = ""

        try:
            input = r.recognize_whisper(audio_data=audio, model="base")
            print("You input : "+input)
            if input == ("Bye.").lower().strip():
                print("See you later")
                exit(0)
            # else:
            #     getAudio()
        except Exception as e:
            print("Exception : "+str(e))
    return input

def manageTextForSarvaam(text, language, filename, gender):
    chunks = get_chunks(text, 499)
    audio_clips = []
    # Print chunks:
    for num, chunk in enumerate(chunks, start=1):
        print({"#": num, "len": len(chunk), "chunk": chunk})
        audio_clips.append(createAudioWithSarvaamBulbulV1(chunk, language, filename+f"_{num}.mp3", gender))
    print(audio_clips)
    final_audio = concatenate_audio_moviepy(audio_clips, "audio/"+filename+".mp3")
    return final_audio

def createAudioWithSarvaamBulbulV1(text, lang, filename, gender):
    print("Text input to Bulbul : "+text)
    url = "https://api.sarvam.ai/text-to-speech"

    lang = getSarvamLanguageCode(lang)

    if gender == "male":
        voice = "amol"
    elif gender == "female":
        voice = "meera"
    
    payload = {
        "inputs": [f'{text}'],
        "target_language_code": f'{lang}',
        "speaker": voice,
        "pitch": 0,
        "pace": 0.9,
        "loudness": 1.5,
        "speech_sample_rate": 8000,
        "enable_preprocessing": True,
        "model": "bulbul:v1"
    }
    headers = {"Content-Type": "application/json", "api-subscription-key":os.getenv("SARVAM_API_KEY") }

    response = requests.request("POST", url, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:

        audio_ascii = json.loads(response.text)["audios"][0]
        print("----+++------")
        print(type(audio_ascii))

        # audio_bytes = bytes(audio_ascii, 'utf-8') # didn't work

        # Decode the Base64 encoded audio
        audio_bytes = base64.b64decode(audio_ascii)
        print("----+++------")
        print(type(audio_bytes))

        # Define the directory and file path
        directory = "audio"
        audio_file = getFilePath(directory, filename)
        
        # Save the decoded audio to a WAV file
        with open(audio_file, "wb") as f:
            f.write(audio_bytes)
            # playsound.playsound(audio_file)

        # s3AudioFile = getS3FilePath(audio_file)
        print(f"Audio saved as '{audio_file}'.")
        return audio_file
    else:
        print(f"Failed to get audio from API. Status code: {response.status_code}, Response: {response.text}")
        return None


# if __name__ == "__main__":
#     input = """Friction is a force that opposes motion between two surfaces in contact. There are different types of friction, each with its own characteristics and causes. **Static friction** acts on objects at rest, preventing them from moving. Think of a heavy box on the floor—you need to apply force to overcome static friction and get it moving. Once the object starts moving, **kinetic friction** takes over, opposing the object's motion.  Imagine sliding that box across the floor—the force you need to keep it moving is kinetic friction.  **Rolling friction** occurs between a rolling object and the surface it's rolling on, like a car's tires on the road.  It's generally less than sliding friction, which is why rolling objects move more easily. Finally, **fluid friction**, also known as drag, occurs when an object moves through a fluid, like air or water.  This type of friction is what slows down a plane or a swimmer."""
#     # textToAudio(input,"../gemini_langgraph_fastapi/course_creation/audio/","file3.mp3", "female") 
#     tinput = translateText(input,'hindi')
#     WhisperAudioTool()._run([tinput, "hindi", "friction_audio"])