import json
import os
from dotenv import load_dotenv
import requests

load_dotenv(os.getcwd()+"/local.env")

def translateText(input, slanguage, tlanguage):

    print(f"Text for Translation : {input}")

    url = "https://api.sarvam.ai/translate"

    if slanguage == None:
        slanguage = "en-IN"

    payload = {
        "input": input,
        "source_language_code": slanguage,
        "target_language_code": getSarvamLanguageCode(tlanguage),
        "speaker_gender": "Male",
        "mode": "formal",
        "model": "mayura:v1",
        "enable_preprocessing": True
    }
    headers = {"Content-Type": "application/json",  "api-subscription-key":os.getenv("SARVAM_API_KEY") }

    response = requests.request("POST", url, json=payload, headers=headers)

    # print(response.text)

    return (json.loads(response.text)["translated_text"])

def getSarvamLanguageCode(language):
    code = "en-IN"
    if language.lower() == 'kannada':
        code = "kn-IN"
    if language.lower() == 'hindi':
        code = "hi-IN"
    # if language.lower() == 'english':
    #    lang = "en-IN"
    print(code)
    return code

if __name__ == "__main__":
    input = "तकनीकें हमारे"
    res = translateText(input, "hi-IN", "English")
    print(res)