import http.client
import json
from typing import TypeVar, Generic
from entities.clouds import AivenClouds

T = TypeVar('T')  
class Result(Generic[T]):
    def __init__(self, status: int, body: T):
        self.status = status
        self.body = body

class ExternalApi:
    def __init__(self):
        pass
    
    # throws exceptions
    def get_clouds(self) -> Result[AivenClouds]:
        conn = http.client.HTTPSConnection("api.aiven.io")
        conn.request("GET", "/v1/clouds")
        response = conn.getresponse()

        respone_body = json.loads(response.read().decode())
        return Result(
            response.status, 
            AivenClouds(
                **respone_body
            )
        )