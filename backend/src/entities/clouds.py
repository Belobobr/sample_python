from pydantic import BaseModel
from geo.geo import Point
from typing import Optional

class Cloud(BaseModel):
    cloud_description: str
    cloud_name: str
    geo_latitude: int
    geo_longitude: int
    geo_region: str
    provider: str
    provider_description: str

    def as_point(self) -> Point:
        return Point(
            latitude=self.geo_latitude,
            longitude=self.geo_longitude,
        )
    
class CloudRequestFilter(BaseModel):
    provider: str

class CloudRequestSort(BaseModel):
    user_geo_latitude: float
    user_geo_longitude: float

    def as_point(self) -> Point:
        return Point(
            latitude=self.user_geo_latitude,
            longitude=self.user_geo_longitude,
        )

class SearchCloudsRequest(BaseModel):
    filter: Optional[CloudRequestFilter]
    sort: Optional[CloudRequestSort]

