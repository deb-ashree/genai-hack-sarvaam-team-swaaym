from typing_extensions import List, Optional, TypedDict
from pydantic import BaseModel, HttpUrl

class SectionState(BaseModel):  #TypedDict, total=False
    main_topic : Optional [str] = None
    section_name :  Optional [str] = None
    section_details :  Optional [str] = None
    course_images :  Optional [list[HttpUrl]] = None
    # research_data: str | None
    section_summary:  Optional [str] = None
    section_review:  Optional [str] = "Pending"
    summaryVideoURL:  Optional [HttpUrl] = None # "link for the video URL"# 
    textContentAudioEnURL :  Optional [HttpUrl] = None # "link for the English audio URL" #