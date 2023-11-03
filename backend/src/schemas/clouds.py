from enum import StrEnum
from pydantic import BaseModel
from typing import Optional
from external_api.clouds import AivenClouds
from geo.geo import Point

class CloudRequestFilter(BaseModel):
    provider: str

class CloudRequestSort(BaseModel):
    user_geo_latitude: float
    user_geo_longitude: float

    # TODO what should i use instead of kotlin extension functions?

    # @classmethod
    # def from_point(point: Point):
    #     return CloudRequestSort(
    #         user_geo_latitude=point.latitude,
    #         user_geo_longitude=point.longitude,
    #     )

    def as_point(self) -> Point:
        return Point(
            latitude=self.user_geo_latitude,
            longitude=self.user_geo_longitude,
        )

class SearchCloudsRequest(BaseModel):
    filter: Optional[CloudRequestFilter]
    sort: Optional[CloudRequestSort]

class SearchCloudsResponse(AivenClouds):
    pass
