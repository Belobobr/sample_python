import asyncio
from typing import Optional, List

from external_api.index import ExternalApi
from external_api.clouds import AivenClouds, AivenCloud
from schemas.clouds import SearchCloudsRequest, SearchCloudsResponse
from geo.geo import get_distance_between_two_points, Point

# should be singleton
class CloudsService:
    external_api: ExternalApi
    cached_clouds: Optional[AivenClouds]

    def __init__(self, external_api: ExternalApi):
        self.external_api = external_api
        self.cached_clouds = None
        self.get_clouds_from_external_service_in_progress_condition = None

    # def get_aiven_clouds(self) -> Result[AivenClouds]:
    #     return get_aiven_clouds()
    
    def get_clouds(self) -> Optional[AivenClouds]:
        try:
            result = self.external_api.get_clouds()
            if result.status == 200:
                return result.body
            return None
        except Exception as e:
            return None
        
    async def get_clouds_cached(self) -> Optional[AivenClouds]:
        if self.cached_clouds is None:
            if self.get_clouds_from_external_service_in_progress_condition:
                # print(f"ext_wait self.get_clouds_from_external_service_in_progress_condition, let's wait")
                async with self.get_clouds_from_external_service_in_progress_condition:
                    await self.get_clouds_from_external_service_in_progress_condition.wait()
                # print(f"ext_wait self.get_clouds_from_external_service_in_progress_condition, finished waiting")
            else:
                # print(f"ext_create self.get_clouds_from_external_service_in_progress_condition not in progress, let's call")
                self.get_clouds_from_external_service_in_progress_condition = asyncio.Condition()
                clouds = await self.get_clouds()
                self.cached_clouds = clouds
                async with self.get_clouds_from_external_service_in_progress_condition:
                    self.get_clouds_from_external_service_in_progress_condition.notify_all()
                self.get_clouds_from_external_service_in_progress_condition = None

        return self.cached_clouds
    
    def search_clouds(self, search_clouds_request: SearchCloudsRequest) -> Optional[SearchCloudsResponse]:
        clouds_response = self.get_clouds()

        if clouds_response == None:
            return None
        
        clouds = clouds_response.clouds
        if search_clouds_request.filter is not None:
            clouds = [cloud for cloud in clouds if cloud.provider == search_clouds_request.filter.provider]

        if search_clouds_request.sort is not None:
            clouds = self.sort_clouds_by_closest_to_user(search_clouds_request.sort.as_point(), clouds)

        return SearchCloudsResponse(
            clouds=clouds,
            errors=clouds_response.errors,
            message=clouds_response.message,
        )

    def sort_clouds_by_closest_to_user(self, user_point: Point, clouds: List[AivenCloud]) -> List[AivenCloud]:
        return sorted(
            clouds,
            key=lambda cloud: get_distance_between_two_points(
                user_point,
                cloud.as_point()
            )
        )
        