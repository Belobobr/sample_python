from typing import List, Optional
from pydantic import BaseModel
from geo.geo import Point

class AivenCloud(BaseModel):
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

class AivenError(BaseModel):
    message: str
    more_info: str
    status: int

class AivenClouds(BaseModel):
    clouds: List[AivenCloud]
    errors: Optional[List[AivenError]] = None
    message: Optional[str] = None


