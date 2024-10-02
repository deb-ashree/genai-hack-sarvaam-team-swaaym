from textwrap import dedent
import time, os
from dotenv import load_dotenv
import requests
from langchain.tools import tool, BaseTool

import asyncio

from requests import HTTPError


load_dotenv(os.getcwd()+"/course_creation/local.env")


did_api_key = os.getenv("D-ID_API_KEY")

## ------For Video Generation---------
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization" : "Basic "+ did_api_key  #os.getenv("D-ID_API_KEY")
}

url = "https://api.d-id.com/clips"

class DIDVideoTool(BaseTool):
    name: str = "D-ID Video generation tool"
    description: str = "This tool generates and retrieves the video for a summary explanation on a specific topic."

    def _run(self, argument: str) -> str:
        try: 
            return asyncio.run(getSummaryVideo(argument)) #asyncio.run()
        except Exception as E:
            raise Exception(E) from E


#@tool("DIDVideoTool")
# def getSummaryVideoURL():
#     return asyncio.run(getSummaryVideo)

async def getSummaryVideo(audioUrl):
    print('postCreateDIDTalkVideo start')
    id = postCreateDIDTalkVideo(audioUrl)
    await asyncio.sleep(240)
    # id ="clp_c4nDNYNwgLFwssfKiHn5-"
    videoURL = getTalkVideo(id)

    print('VideoURL received '+videoURL)
    return videoURL


def postCreateDIDTalkVideo(audioUrl):
    print("At payload")
    payload = {
        "script": {
            "type": "audio",
            "subtitles": "false",
            "ssml": "false",
            "audio_url": audioUrl
        },
        "presenter_id": "lily-akobXDF34M",
        "driver_id": "oqNen3Q3aS",
        "source_url": "https://clips-presenters.d-id.com/lily/akobXDF34M/oqNen3Q3aS/image.png",
        # "https://gen-ai-data.s3.us-west-2.amazonaws.com/Instructor1.jpeg",
        #"https://www.thesun.co.uk/wp-content/uploads/2021/10/2394f46a-c64f-4019-80bd-445dacda2880.jpg?w=670", ##lily-akobXDF34M
        "config": {
                "result_format": "mp4",
                "driver_expressions": {
                "expressions": [
                    # {
                    #     "start_frame": 0,
                    #     "expression": "surprise",
                    #     "intensity": 1.0
                    # },
                    {
                        "start_frame": 0,
                        "expression": "happy",
                        "intensity": 1.0
                    }
                ],
                "transition_frames": 20
            }
        },
        # "config": { "result_format": "mp4" },
        "presenter_config": { "crop": { "type": "wide" } },
        "background": {"source_url": "https://gen-ai-data.s3.us-west-2.amazonaws.com/joe-woods-4Zaq5xY5M_c-unsplash.jpg"}
    }
    print("Post payload...")
    try:
        print("Inside try..")
        post_response = requests.post(url, json=payload, headers=headers)
        print(post_response)
        if post_response.status_code == 201:
            print("Inside 201")
            print(post_response.text)
            res = post_response.json()
            id = res["id"]
            print(f"Id : "+id)
            print(res)
            status = "created"
            return id
    except HTTPError as e:
        print(e.response.text)

def getTalkVideo(id):
    fetch_url = "https://api.d-id.com/talks/"+id
    try:
        get_response = requests.get(url, headers=headers)
        print(get_response)
        if get_response.status_code == 200:
            video_url = get_response.json()["clips"][0]["result_url"]  
            print("Video "+video_url)
        return video_url
    except Exception as e:
        print(e)      
        video_url = "error"      

def main():
    # summaryText = dedent("""Evaporation is the process where a liquid turns into a gas. You can see it happening when water in a puddle 
    #                      disappears on a hot day. The heat from the sun turns the water into an invisible gas called water vapor, which 
    #                      rises into the air. This is how clouds are formed! Let's get into further details. """)
    # summaryText = dedent("""Friction is a force that opposes motion between two surfaces in contact. There are different types of friction, each with its own characteristics and causes. 
    #                      **Static friction** acts on objects at rest, preventing them from moving. Think of a heavy box on the floor\u2014you need to apply force to overcome static friction and get it moving. Once the object starts moving, 
    #                      **kinetic friction** takes over, opposing the object's motion.  Imagine sliding that box across the floor\u2014the force you need to keep it moving is kinetic friction.  
    #                      **Rolling friction** occurs between a rolling object and the surface it's rolling on, like a car's tires on the road.  It's generally less than sliding friction, which is why rolling objects move more easily. 
    #                      Finally, **fluid friction**, also known as drag, occurs when an object moves through a fluid, like air or water.  This type of friction is what slows down a plane or a swimmer."
    #                      """)
    # asyncio.run(getSummaryVideo("https://gen-ai-data.s3.amazonaws.com/%E0%A4%98%E0%A4%B0%E0%A5%8D%E0%A4%B7%E0%A4%A3_%E0%A4%95%E0%A5%87_%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%95%E0%A4%BE%E0%A4%B0_audio.mp3"))
    asyncio.run(getSummaryVideo("https://gen-ai-data.s3.amazonaws.com/Friction_summary_audio1.mp3"))
    # getTalkVideo("clp_UswC9ThrMbmRkOQxOfnUh")
    # getTalkVideo("clp_c4nDNYNwgLFwssfKiHn5-")
   

if __name__ == "__main__":
     main()



# payload = {
#         "script": {
#             "type": "audio",
#             "subtitles": "true",
#             "input": summarytext,
#             "provider": {
#                 "type": "microsoft",
#                 "voice_id": "en-US-JennyNeural"
#             },
#             "ssml": "false"
#         },
#         "presenter_id": "lily-akobXDF34M",
#         "driver_id": "oqNen3Q3aS",
#         "source_url": "https://clips-presenters.d-id.com/lily/akobXDF34M/oqNen3Q3aS/image.png",
#         # "https://gen-ai-data.s3.us-west-2.amazonaws.com/Instructor1.jpeg",
#         #"https://www.thesun.co.uk/wp-content/uploads/2021/10/2394f46a-c64f-4019-80bd-445dacda2880.jpg?w=670", ##lily-akobXDF34M
#         "config": {
#                 "result_format": "mp4",
#                 "driver_expressions": {
#                 "expressions": [
#                     # {
#                     #     "start_frame": 0,
#                     #     "expression": "surprise",
#                     #     "intensity": 1.0
#                     # },
#                     {
#                         "start_frame": 0,
#                         "expression": "happy",
#                         "intensity": 1.0
#                     }
#                 ],
#                 "transition_frames": 20
#             }
#         },
#         # "config": { "result_format": "mp4" },
#         "presenter_config": { "crop": { "type": "wide" } },
#         "background": {"source_url": "https://gen-ai-data.s3.us-west-2.amazonaws.com/joe-woods-4Zaq5xY5M_c-unsplash.jpg"}
#     }