# Set up the state
import json
import os
from IPython.display import Image, display
# from PIL import Image
from typing import TypedDict
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.checkpoint.memory import MemorySaver

from langgraph.constants import Send

from data_models.data_collation_object import TopicState
from graphs.data_collation_nodes import DataCollectionNode

class CourseContentFlow():

    def __init__(self, model):
        self.model = model
        # self.input = input

    # Here we define the logic to map out over the generated subjects
    # We will use this an edge in the graph
    def continue_to_sections(self, state: TopicState):
        # We will return a list of `Send` objects
        # Each `Send` object consists of the name of a node in the graph
        # as well as the state to send to that node
        print(f"State received in graph loop \n {state}")
        return [Send("collateContent", {"section_name": s.section_name}) for s in state["sections"]]
        # section_list = state["sections"]
        # for s in section_list:
        #     output = Send("collateContent", {"section_name": s.section_name})
        #     print(f" Output from Send : \n{output}")
        #     outputJson = json.loads(f"{output}") #.format("response.choices[0].message.content")
        #     print(f"TextContent : {outputJson}")
        #     s.section_summary = outputJson["section_summary"]
        #     s.section_details = outputJson["section_details"]
        # return {"sections" : section_list}

    def runGraph(self):
        # Build the graph

        from langgraph.graph import END, StateGraph

        # Define a new graph
        workflow = StateGraph(TopicState)

        node = DataCollectionNode(self.model)

        # Define the three nodes we will cycle between
        workflow.add_node("courseStart", node.courseStart)
        workflow.add_node("summarize", node.getSummary)
        workflow.add_node("createSections", node.getSections)
        workflow.add_node("plan", node.getPlan)
        # workflow.add_node("research", node.researchSection)
        workflow.add_node("delegator", node.checkSections)
        workflow.add_node("collateCourse", node.collateCourse)
        # workflow.add_node("collate", node.collateCourse)

        # Set the entrypoint as `agent`
        # This means that this node is the first one called
        workflow.support_multiple_edges = True
        workflow.set_entry_point("courseStart")
        workflow.add_edge(START, "courseStart")
        # workflow.add_edge("courseStart", "summarize")
        workflow.add_edge("summarize", "createSections")
        workflow.add_edge("createSections", "plan")
        workflow.add_edge("plan", "delegator")  #,"collateContent"
        workflow.add_edge("delegator", "collateCourse") 
        workflow.add_edge("collateCourse", END)
        workflow.add_conditional_edges(
				"courseStart",
				node.checkForReview,
				{
					"pending": 'summarize',
					"done": 'delegator'
				}
		)

        # Set up memory
        from langgraph.checkpoint.memory import MemorySaver

        memory = MemorySaver()

        # Finally, we compile it!
        # This compiles it into a LangChain Runnable,
        # meaning you can use it as you would any other runnable
        # We add a breakpoint BEFORE the `ask_human` node so it never executes
        app = workflow.compile()   # for HITL  checkpointer=memory, interrupt_before=["ask_human"]

        # display(Image(...,embed=True))
        app.get_graph().draw_png('data_collation_graph_img.png')
        return app