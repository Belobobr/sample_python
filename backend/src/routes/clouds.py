import logging
from fastapi import APIRouter, HTTPException

from config import Config
from schemas.clouds import SearchCloudsRequest, SearchCloudsResponse
from external_api.clouds import ExternalServices

logger = logging.getLogger(__name__)

class CloudRouterDependencies:
    def __init__(self, external_services: ExternalServices):
        self.external_services = external_services

    external_services: ExternalServices

def create_cloud_router_dependencies(
        config: Config, 
        external_services: ExternalServices
) -> CloudRouterDependencies:
    return CloudRouterDependencies(
        external_services=external_services,
    )

def create_clouds_router(config: Config, dependencies=CloudRouterDependencies):

    async def search_clouds(
        search_request: SearchCloudsRequest,
    ) -> SearchCloudsResponse:
        result = dependencies.external_services.get_clouds()

        if result.status == 200 and result.body.errors is None:
            return SearchCloudsResponse(
                clouds=result.body.clouds
            )

        raise HTTPException(status_code=503, detail="Service is unavailable") 

    router = APIRouter()
    router.post(
        "/clouds:search",
        response_model=SearchCloudsResponse,
    )(search_clouds)
    return router