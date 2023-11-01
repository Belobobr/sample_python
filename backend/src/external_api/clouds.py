import http.client
import json
from typing import TypeVar, Generic, List, Optional
# from pydantic.dataclasses import dataclass
from pydantic import BaseModel
from geo.geo import Point

# @dataclass
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

# @dataclass
class AivenError(BaseModel):
    message: str
    more_info: str
    status: int

# @dataclass
class AivenClouds(BaseModel):
    clouds: List[AivenCloud]
    errors: Optional[List[AivenError]] = None
    message: Optional[str] = None

T = TypeVar('T')  
class Result(Generic[T]):
    def __init__(self, status: int, body: T):
        self.status = status
        self.body = body

# TODO
# add caching (in memory)
# add circuit breaker
class ExternalApi:
    def __init__(self):
        pass

    # def get_aiven_clouds(self) -> Result[AivenClouds]:
    #     return get_aiven_clouds()
    
    def get_clouds(self) -> Result[AivenClouds]:
        conn = http.client.HTTPSConnection("api.aiven.io")
        conn.request("GET", "/v1/clouds")
        response = conn.getresponse()
        # return response

        respone_body = json.loads(response.read().decode())
        return Result(
            response.status, 
            AivenClouds(
                **respone_body
            )
        )

def create_external_services() -> ExternalApi:
    return ExternalApi()
