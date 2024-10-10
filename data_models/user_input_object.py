from typing_extensions import List
from pydantic import BaseModel, HttpUrl

class UserInput(BaseModel):  #TypedDict, total=False
    grade : str
    subject : str
    topic : str 
    language : str
    instructions : str
    review_status : str
    