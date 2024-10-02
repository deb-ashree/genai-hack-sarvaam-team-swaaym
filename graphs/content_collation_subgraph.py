import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END

from data_models.data_sections_object import SectionState

load_dotenv()

class CourseSubSectionFlow():
	def __init__(self, nodes):
		print("At init..")
		workflow = StateGraph(SectionState)
		print("init..sub 1")

		## // Nodes
		#nodes = Nodes()
		print(nodes)
		# workflow.add_node("courseSectionStart", nodes.courseSectionStart)
		workflow.add_node("collateTextContent", nodes.collateTextContent)
		## Calls crew for execution of Research and Content Creation Tasks
		workflow.add_node("videoGenerator", nodes.createSummaryVideo)
		workflow.add_node("audioGenerator", nodes.createTextAudioContentEN)
		workflow.add_node("storypicker", nodes.pickStoryVideo)
		workflow.add_node("mergeFlow", nodes.mergeFlow)
		print("init..sub 2")
	
		## // Edges
		workflow.support_multiple_edges = True
		workflow.set_entry_point("collateTextContent")
		workflow.add_conditional_edges(
				"collateTextContent",
				nodes.checkForSectionReview,
				{
					"pending": 'mergeFlow',
					"done": 'audioGenerator'
				}
		)
		workflow.add_edge('collateTextContent', 'mergeFlow')
		workflow.add_edge('audioGenerator', 'videoGenerator')
		workflow.add_edge('audioGenerator', 'storypicker')
		workflow.add_edge(['videoGenerator', 'storypicker'], 'mergeFlow')
		workflow.add_edge('mergeFlow', END)
		
		print("init..sub 3")
		print(workflow.nodes)
		print(workflow.schema)
		
		self.app = workflow.compile()
		print("init..compiled")

		# Graph Visualization
		# os.environ["PATH"] += os.pathsep + '/opt/homebrew/bin'
		# Image(workflow.get_graph().draw_png())

# def displayWorkflow(graph):
		# from IPython.display import Image, display
		self.app.get_graph().draw_png("data_collation_subgraph_img.png")
		# self.app.get_graph().draw_mermaid_png('data_collation_subgraph_img.png', curve_style=CurveStyle.LINEAR,node_colors=NodeStyles(first="#ffdfba", last="#baffc9", default="#fad7de"), background_color="white")