from pydantic import BaseModel
from geo.geo import Point

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

