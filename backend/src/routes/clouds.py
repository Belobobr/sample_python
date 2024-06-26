import logging

from api.payload import BodyClouds
from config import Config
from entities.clouds import SearchClouds
from fastapi import APIRouter, HTTPException
from services.cloud import CloudsService

logger = logging.getLogger(__name__)

class CloudRouterDependencies:
    def __init__(self, cloud_service: CloudsService):
        self.cloud_service = cloud_service
    cloud_service: CloudsService

def create_cloud_router_dependencies(
        config: Config, 
        cloud_service: CloudsService
) -> CloudRouterDependencies:
    return CloudRouterDependencies(
        cloud_service=cloud_service,
    )

def create_clouds_router(config: Config, dependencies=CloudRouterDependencies):

    async def search_clouds(
        search_request: SearchClouds,
    ) -> BodyClouds:
        result = await dependencies.cloud_service.search_clouds(search_request)

        if result is not None:
            return result

        raise HTTPException(status_code=503, detail="Service is unavailable") 

    router = APIRouter()
    router.post(
        "/clouds:search",
        response_model=BodyClouds,
    )(search_clouds)
    return router