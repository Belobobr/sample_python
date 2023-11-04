from typing import Optional
from locust import HttpUser, task, between

# class CloudRequestFilter():
#     provider: str

# class CloudRequestSort():
#     user_geo_latitude: float
#     user_geo_longitude: float

# class SearchCloudsRequest():
#     filter: Optional[CloudRequestFilter]
#     sort: Optional[CloudRequestSort]

class SearchCloudsUser(HttpUser):
    wait_time = between(5, 15)
    
    @task
    def search(self):
        self.client.post(
            "/api/clouds:search", 
            json={}
        )

    @task
    def search_with_filter(self):
        self.client.post(
            "/api/clouds:search", 
            json={
                "filter": {
                    "provider": "aws"
                },
            }
        )

    @task
    def search_with_filter_and_sort(self):
        self.client.post(
            "/api/clouds:search", 
            json={
                "filter": {
                    "provider": "aws"
                },
                "sort": {
                    "user_geo_latitude": -33,
                    "user_geo_longitude": 150
                }
            }
        )