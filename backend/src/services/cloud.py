import logging
import asyncio
from typing import Optional, List

from api.external import ExternalApi
from entities.clouds import Cloud
from api.payload import AivenClouds
from schemas.clouds import SearchCloudsRequest, SearchCloudsResponse
from geo.geo import get_distance_between_two_points, Point

logger = logging.getLogger(__name__)

# should be singleton

# caching options
# - cache all clouds, compute distance on the fly
# - create tile map of the world, 
# compute distance between tiles once, 
# map clouds to tiles, 
# compute closest clouds for every tile,
# store closest clouds for every tile in cache
class CloudsService:
    external_api: ExternalApi
    cached_clouds: Optional[AivenClouds]

    def __init__(self, external_api: ExternalApi):
        self.external_api = external_api
        self.cached_clouds = None
        self.get_clouds_from_external_service_in_progress_condition = None
    
    async def get_clouds(self) -> Optional[AivenClouds]:
        try:
            result = self.external_api.get_clouds()
            if result.status == 200:
                return result.body
            return None
        except Exception as e:
            return None
        
    # cache eviction policy
    async def get_clouds_cached(self) -> Optional[AivenClouds]:
        if self.cached_clouds is None:
            logger.info(f"clouds are not in cache")

            if self.get_clouds_from_external_service_in_progress_condition:
                logger.info(f"wait for receiving clouds from external service")
                async with self.get_clouds_from_external_service_in_progress_condition:
                    await self.get_clouds_from_external_service_in_progress_condition.wait()
            else:
                logger.info(f"receive clouds from external service")
                self.get_clouds_from_external_service_in_progress_condition = asyncio.Condition()
                clouds = await self.get_clouds()
                self.cached_clouds = clouds
                async with self.get_clouds_from_external_service_in_progress_condition:
                    self.get_clouds_from_external_service_in_progress_condition.notify_all()
                self.get_clouds_from_external_service_in_progress_condition = None

            return self.cached_clouds
        else:
            logger.info(f"clouds are in cache")
            return self.cached_clouds
    
    async def search_clouds(self, search_clouds_request: SearchCloudsRequest) -> Optional[SearchCloudsResponse]:    
        clouds_response = await self.get_clouds_cached()

        if clouds_response == None:
            return None
        
        clouds = clouds_response.clouds
        if search_clouds_request.filter is not None:
            logger.info(f"filter clouds for request {search_clouds_request}")
            clouds = [cloud for cloud in clouds if cloud.provider == search_clouds_request.filter.provider]

        if search_clouds_request.sort is not None:
            logger.info(f"sort clouds for request {search_clouds_request}")
            clouds = self.sort_clouds_by_closest_to_user(search_clouds_request.sort.as_point(), clouds)

        logger.info(f"return clouds for request {search_clouds_request}")
        return SearchCloudsResponse(
            clouds=clouds,
            errors=clouds_response.errors,
            message=clouds_response.message,
        )

    def sort_clouds_by_closest_to_user(self, user_point: Point, clouds: List[Cloud]) -> List[Cloud]:
        return sorted(
            clouds,
            key=lambda cloud: get_distance_between_two_points(
                user_point,
                cloud.as_point()
            )
        )
    

        