from enum import StrEnum
from pydantic import BaseModel
from typing import Optional
# from pydantic.dataclasses import dataclass
from external_services.clouds import AivenClouds

class SortField(StrEnum):
    DISTANCE_FROM_USER = "distance_from_user"

# @dataclass
class CloudFilter(BaseModel):
    povider: str

# @dataclass
class CloudRequestFilter(BaseModel):
    user_geo_latitude: int
    user_geo_longitude: int
    cloud: CloudFilter

# @dataclass
class SearchCloudsRequest(BaseModel):
    filter: Optional[CloudRequestFilter]
    sort: Optional[SortField]

# @dataclass
class SearchCloudsResponse(AivenClouds):
    pass