from enum import StrEnum
from pydantic import BaseModel
from typing import Optional
from external_services.clouds import AivenClouds

class SortField(StrEnum):
    DISTANCE_FROM_USER = "distance_from_user"

class CloudRequestFilter(BaseModel):
    provider: str

class CloudRequestSort(BaseModel):
    user_geo_latitude: int
    user_geo_longitude: int

class SearchCloudsRequest(BaseModel):
    filter: Optional[CloudRequestFilter]
    sort: Optional[CloudRequestSort]

class SearchCloudsResponse(AivenClouds):
    pass