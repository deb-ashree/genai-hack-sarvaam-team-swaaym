import json, os
import re
from typing import TypedDict
from dotenv import load_dotenv
from textwrap import dedent

from pydantic import BaseModel
from graphs.content_collation_subgraph import CourseSubSectionFlow
from tools.AudioTools import WhisperAudioTool
from tools.VideoTools import DIDVideoTool
from tools.tools import duckduckgo_search
from tools.TextTools import translateText
# from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai

from data_models.data_collation_object import TopicState
from data_models.data_sections_object import SectionState
# from langchain.output_parsers import PydanticOutputParser
print(os.getcwd())
load_dotenv(os.getcwd()+"/course_creation/local.env")

# class SubSectionState(TypedDict):
#     section: str

class SectionContent(BaseModel):
    section_details: str
    section_summary: str


class DataCollectionNode():

    def __init__(self, model) -> None:
        self.model = model
        # self.input = input
        self.topic = None
        self.language = "English"
        self.i = 0
	
    def getResponse(self, prompt): 
        response = self.model.invoke(prompt)
        print(f"Response : {response}")
        return response.content
		
    # define nodes

    # def getInputs(self, input: UserInput):
    #     return {"input" : input}

    def getSummary(self,state: TopicState):
        self.topic = state["input"]["topic"]
        print("Main Topic : "+self.topic)
        prompt = f"Provide short summary of 700-120 words for the given topic {self.topic} explaining it in a socratic way to dervive the topic's understanding for the kids of age 9-12 years. Keep the explanantion between 50-60 words only."
        
        response = self.getResponse(prompt)
        if self.language != "English":
            response = translateText(self.getResponse(prompt), None, self.language)
            print(f"Translated Summary {response}")
        return {"summary": response, "topic" : self.topic}

    def getSections(self, state: TopicState):
        prompt = f"Provide 3 sub-topics for the given topic {self.topic} for the course generation. Keep each topic title to 1-3 words only. Output a comma delimited list of the sub-topics Only. " #.
        response = self.getResponse(prompt)
        sections_list = re.sub(r'\*\-\\n', '', response).lstrip().rstrip().split(",")
        if self.language != "English":
            sections_list = [translateText(item, None, self.language) for item in sections_list] #translateText(sections_list, None, self.language)
        print(f" List of sections : {sections_list}")
        return {"sections_list": sections_list}
   
    def getPlan(self, state: TopicState):
        sections = state["sections_list"]
        prompt = f"Create a bulleted lesson plan of the topic {self.topic} based on the sections in {sections}, keep the explanation short, simple, easy to understand and kid-friendly. Each section can have 3 sub sections from any of these - Details, Types, Experiments, Applicability or Real-life examples "
        response = self.getResponse(prompt)
        if self.language != "English":
            response = translateText(response, None, self.language)
        return {"course_plan": response}
    
    def checkSections(self, state: TopicState):
        print(state)
        content_dict = [] #defaultdict(set)
        review_status = state["input"]["review_status"]
        try:
            if(review_status == "Pending"):
                sectionList = state['sections_list'] if state['sections_list'] else []
                if len(sectionList) == 0:
                    print("## No section list found")
                    return "end"
                else:
                    print("## Sections List present")
                    print("Calling Crew..")
                    print(sectionList)
                    print("State : ")
                    print(state)
                    for section in sectionList:        #.split(",")
                        print(f"This is : {section}")
                        subTopic = SectionState(main_topic=self.topic,section_name=section,section_review=review_status,section_summary=None,section_details=None, summaryVideoURL=None, textContentAudioEnURL=None )
                        chain = CourseSubSectionFlow(self).app
                        section = chain.invoke(subTopic)
                        print("Subgrapgh called...\n SectionList :")
                        print(section)
                        content_dict.append(section)
                        print(f"Sections Appended : {content_dict}")
                        print(state)
            else:
                sections = state['sections'] if state['sections'] else []
                if len(sections) == 0:
                    print("## No sections found")
                    return "end"
                else:
                    print("## Sections List present")
                    for section in sections:
                        ## Using Langgraph subgraph
                        chain = CourseSubSectionFlow(self).app
                        section = chain.invoke(section)
                        print("Subgrapgh called...\n Sections :")
                        print(section)
                        content_dict.append(section)
                        print(f"Sections Appended : {content_dict}")
                        print(state)
            print("Dict SubTopic data :")
            print(content_dict)
            return {"sections": content_dict}
        except Exception as E:
            raise Exception(E) from E

    def collateCourse(self, state: TopicState):
        print(f"Final state : {state}")
    #     summary = self.getSummary()
    #     course_plan = self.getPlan()
    #     content_dict = []
    #     course_sections = state["sections"]

    #     content_dict.append(subState)
    #     response = {"summary" : summary, "course_plan" : course_plan, "course_sections" : course_sections}
	
	## research task used internally

    def mergeFlow(self, state: SectionState):
        print(f"Merge section data : {state}")

    def researchSection(self, section):
        print("Calling for research ...")
        print("prompt received..")
        # rag_tool
        researcher_tools = [duckduckgo_search]  # rag_tools to be added
        researcher_prompt =  dedent(f"""
                            You are an experienced researcher who will research and collate the appropriate and relevant content 
                            for the give topic {self.topic} for the section '{section}'. Structure the content with general introduction, purpose, 
                            key topics with a real-life example across, and a final applicable implementation for user to practice.                          
                            Keep the response professional and conversational with a friendly demeanour """)
        model_tools = self.model.bind(functions=researcher_tools)
        data = model_tools.invoke(researcher_prompt)

        # response = client.chat.completions.create(
        #     model=self.llm,
        #     #max_tokens=1024,
        #     messages=[
        #         #{"role": "system", "content": "You are a helpful assistant.Provide details only as requested"},
        #         {"role": "user", "content": dedent(f"""
        #         You are an experienced researcher who will research and collate the appropriate and relevant content 
        #         for the give topic '{sub_topic}'. Structure the content with general introduction, areas of utilization or purpose, 
        #         key topics with a real-life example across, and a final applicable implementation for user to practice. 
        #         Keep the response professional and conversational with a friendly demeanour """)},
        #         {"role": "system", "content": '{response}'}
        #     ]
        # )
        return data.content #  {"research_data" : data}

    ## content generation
    def collateTextContent(self, state: SectionState):  #
        self.i += 1
        if state.section_review != "Done":
            print("Calling for content generation ...")
            print("prompt received..")
            section = state.section_name
            print(section)
            print(f"Received Section value : {section}")
            # research_data = self.researchSection(section)
            # response = section_content_prompt | self.model
            # data = ''
            # if research_data is not '':
            #     data = f"along with the'{research_data}'"
            section_content_prompt = dedent(f""" You are an experienced content creator who will 
                        collate the very specific information for the given topic {section} as a section goal of the main topic {self.topic} 
                        into appropriate section with simple, concise and relevant content. 
                        Structure the content into 90-120 words in paragraph format of simple English content under 'section_details' 
                        and a summary paragraph of max 50 words under 'section_summary' . 
                        Keep the response professional and conversational with a friendly demeanour. The output 
                        should be the formatted as JSON  """ )  #Rest other fields can be as is. Do not add any data to the textContentAudioEnURL or summaryVideoURL fields. in the fields 'section_summary', 'section_details' only. Please provide any code/programming example in a code interpreter with a grey screen under codeExample, IF ONLY there are any relevant examples. #and 'codeExample'
            print(f"Prompt at Collate Section Text : {section_content_prompt}")
            # structured_llm = self.model.with_structured_output(SectionContent, include_raw=True)
            # response = structured_llm.invoke(section_content_prompt)
            genai.configure(api_key = os.environ['GEMINI_API_KEY'])
            model = genai.GenerativeModel('gemini-1.5-flash')  #,generation_config={"response_mime_type": "application/json"})  
            response = model.generate_content( section_content_prompt,
                                                    generation_config=genai.GenerationConfig(response_mime_type="application/json",
                                            response_schema = SectionContent))

            ## Not needed due to above implementation
            # response = self.model.invoke(section_content_prompt)
            # parsed_response = (response.content.replace("```json","")).replace("```","").replace("}","").replace("{","").replace("**","").replace("\'"," ")
            # print(f" Parsed Json Content : \n{parsed_response}")
            # jsonContent = json.loads(f"{parsed_response}") #.format("response.choices[0].message.content")
            # print(f"Summary at generateTextContent : {jsonContent}")
            # state["section_details"] = jsonContent["section_details"]
            # state["section_summary"] = jsonContent["section_summary"]

            # if state["sections"] is None:
            section_list = []
            # section_list.append(state)
            print(f" Response Content : \n{response}")
            # response.replace("\t",",")
            print(f"Section State : {response.text}")
            jsonContent = json.loads(response.text) #.format("response.choices[0].message.content")
            output = {}
            if response is not None and response.text is not None:
                section_details = jsonContent["section_details"]
                if self.language != "English":
                    section_details = translateText(section_details, None, self.language)
                section_summary = jsonContent["section_summary"]
                if self.language != "English":
                    section_summary = translateText(section_summary, None, self.language)
                output = {"main_topic" : self.topic, "section_details" : section_details, "section_summary" : section_summary}
                return output
            # output : SectionState = {"main_topic" : self.topic, "section_name": section, "section_details" : section_details, "section_summary" : section_summary}
            # return {"sections" : [output] }

    def courseSectionStart(self, state:SectionState):
        print(f"Section name : {state.section_name} ")
      
    def courseStart(self, state:TopicState):
        print(f"""Course State : {state["input"]["review_status"]}""")
        self.language = state["input"]["language"]
        self.topic = state["input"]["topic"]
        # if self.language != "English":
        #     self.topic = translateText(state["input"]["topic"], None, self.language)

    def checkForReview(self, state: TopicState):
        print(f"""Review status : {state["input"]["review_status"]}""")
        if state["input"]["review_status"] == "Done":
            return "done"
        else:
            return "pending"
    
    def checkForSectionReview(self, state: SectionState):
        print(f"Section Review status : {state.section_review}")
        if state.section_review == "Done":
            return "done"
        else:
            return "pending"
    
    def createSummaryVideo(self, state: SectionState):
        print("Inside createsummaryvideo ")
        print(state)
        audioURL = WhisperAudioTool()._run([state.section_summary, self.language, f"summary_audio_{self.i}"])  #state.section_name.lstrip().replace(' ','_')
        videoURL = DIDVideoTool()._run(audioURL)
        print(f"video called {videoURL}")
        return {"summaryVideoURL" : videoURL}

    def createTextAudioContentEN(self, state: SectionState):
        print("Inside createcontentaudio ")
        print(state)
        # print(f"Corrected String : "+re.sub("^[a-zA-Z0-9_]*$","",subTopic["textContent"], count=0, flags=0))
        audioURL = WhisperAudioTool()._run([state.section_details, self.language, f"details_audio_{self.i}"])
        print(f"audio called : {audioURL}")
        return {"textContentAudioEnURL" : audioURL}

    def pickStoryVideo(self, state: SectionState):
        print("Inside pickStoryVideo ")
        print(state)
        print("To be implemented")
        # videoURL = DIDVideoTool()._run(state["section_summary"])
        # print(f"video called {videoURL}")
        # return {"summaryVideoURL" : videoURL}

    # def create_tool_node_with_fallback(tools: list) -> dict:
    #     return ToolNode(tools).with_fallbacks(
    #         [RunnableLambda(handle_tool_error)], exception_key="error"
    #     )
    
    # def handle_tool_error(state) -> dict:
    # error = state.get("error")
    # tool_calls = state["messages"][-1].tool_calls
    # return {
    #     "messages": [
    #         ToolMessage(
    #             content=f"Error: {repr(error)}\n please fix your mistakes.",
    #             tool_call_id=tc["id"],
    #         )
    #         for tc in tool_calls
    #     ]
    # }


	# 	print("Response : ")
	# 	print(response)
	# 	# response = dedent("""{\n\t"summary": Certainly! Let\'s delve into the topic of Variables together .\n\nIntroduction:\nVariables play a crucial role in computer programming and data analysis",
	# 	# \n\t"textContent": [\n\t\t"Variables serve as placeholders for storing and manipulating data in programming and statistical analysis. They are indispensable in controlling program flow"}""")
	# 	jsonContent = json.loads(f"{response.choices[0].message.content}") #.format("response.choices[0].message.content")
	# 	print(f"Summary at generateTextContent : {jsonContent}")
	# 	print("at return")
	# 	return {"summary" :jsonContent["summary"], "textContent" :jsonContent["textContent"]}      #, "codeExample" : jsonContent["codeExample"]


## using Gemini for a llm call

        # chat = self.model.start_chat()
        # return chat.send_message(prompt, stream=True)
        #----------
        # chain = prompt | model
        # response = chain.invoke()
        #----------
        # response = model.generate_content(prompt)
        # return response.candidates[0].content.parts[0].text