import logging
from fastapi import APIRouter

from config import Config
from schemas.clouds import SearchCloudsRequest, SearchCloudsResponse

logger = logging.getLogger(__name__)

def creat_clouds_router(config: Config):

    async def search_clouds(
        search_request: SearchCloudsRequest,
    ) -> SearchCloudsResponse:
        return SearchCloudsResponse(
            clouds=[]
        )

    router = APIRouter()
    router.post(
        "/clouds:search",
        response_model=SearchCloudsResponse,
    )(search_clouds)
    return router