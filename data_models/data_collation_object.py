from typing_extensions import List, TypedDict
from pydantic import BaseModel

from data_models.data_sections_object import SectionState

class TopicState(TypedDict, total=False):
    input : dict
    topic : str
    summary : str
    course_plan : str
    sections_list : List[SectionState]
    sections : List[SectionState]