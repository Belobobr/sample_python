from typing import List, Optional
from pydantic import BaseModel
from entities.clouds import Cloud

class BodyError(BaseModel):
    message: str
    more_info: str
    status: int

class BodyClouds(BaseModel):
    clouds: List[Cloud]
    errors: Optional[List[BodyError]] = None
    message: Optional[str] = None


