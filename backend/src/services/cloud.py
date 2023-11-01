import asyncio
from typing import Optional

from external_api.index import ExternalApi
from external_api.clouds import AivenClouds

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
    
    def search_clouds(self):
        pass