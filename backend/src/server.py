import logging
import sys

from fastapi import FastAPI, APIRouter
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from dependencies import ApplicationDependenciesGraph

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

async def validation_exception_handler(request, exc):
    error_messages = []
    for error in exc.errors():
        field = ".".join(str(field) for field in error["loc"])
        error_messages.append({
            "field": field,
            "message": error["msg"]
        })
    return JSONResponse(status_code=422, content={"errors": error_messages})


def create_application(application_dependencies_graph: ApplicationDependenciesGraph) -> FastAPI:
    application = FastAPI()

    api_router = APIRouter()
    api_router.include_router(application_dependencies_graph.health_router)
    api_router.include_router(application_dependencies_graph.clouds_router)

    application.include_router(api_router, prefix="/api")

    application.add_exception_handler(RequestValidationError, validation_exception_handler)
    return application

# TODO
# observability
# cache eviction policy, cache error policy
# check different caching strategy (based on tiles)
# clean structure for api and backend
