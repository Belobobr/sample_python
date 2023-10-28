from fastapi import FastAPI, APIRouter
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from routes.health import create_health_router
from routes.clouds import creat_clouds_router
from config import get_config, Config

async def validation_exception_handler(request, exc):
    error_messages = []
    for error in exc.errors():
        field = ".".join(str(field) for field in error["loc"])
        error_messages.append({
            "field": field,
            "message": error["msg"]
        })

    return JSONResponse(status_code=422, content={"errors": error_messages})

def create_application(config: Config) -> FastAPI:
    health_router = create_health_router(config)
    clouds_router = creat_clouds_router(config)

    application = FastAPI()

    api_router = APIRouter()
    api_router.include_router(health_router)
    api_router.include_router(clouds_router)

    application.include_router(api_router, prefix="/api")
    # application.include_router(health_router)
    # application.include_router(clouds_router)

    application.add_exception_handler(RequestValidationError, validation_exception_handler)
    return application

app = None
if __name__ == "__main__":
    config = get_config()
    app = create_application(config)

# app = FastAPI()
# @app.get("/api/hello")
# async def root():
#     return {"message": "Hello world"}
