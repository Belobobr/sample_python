from typing import List, Optional
from pydantic import BaseModel
from entities.clouds import Cloud

class AivenError(BaseModel):
    message: str
    more_info: str
    status: int

class AivenClouds(BaseModel):
    clouds: List[Cloud]
    errors: Optional[List[AivenError]] = None
    message: Optional[str] = None

class SearchCloudsResponse(AivenClouds):
    pass

