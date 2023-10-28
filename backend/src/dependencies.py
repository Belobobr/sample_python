
from fastapi import APIRouter
from routes.health import create_health_router
from routes.clouds import create_clouds_router, create_cloud_router_dependencies
from external_services.clouds import ExternalServices
from config import Config

class ApplicationDependenciesGraph:

    def __init__(self, health_router: APIRouter, clouds_router: APIRouter):
        self.health_router = health_router
        self.clouds_router = clouds_router

    health_router: APIRouter
    clouds_router: APIRouter

class ApplicationDependencies:
    def __init__(self, health_router: APIRouter, clouds_router: APIRouter):
        self.health_router = health_router
        self.clouds_router = clouds_router

    health_router: APIRouter
    clouds_router: APIRouter

def create_dependencies_graph(config: Config, dependencies=ApplicationDependencies) -> ApplicationDependenciesGraph:
    return ApplicationDependenciesGraph(
        health_router=dependencies.health_router,
        clouds_router=dependencies.clouds_router,
    )

def provide_dependencies_graph(config: Config) -> ApplicationDependenciesGraph:

    clouds_router = create_clouds_router(
        config, 
        dependencies=create_cloud_router_dependencies(
            config, 
            external_services=ExternalServices()
        )
    )

    health_router = create_health_router(config)
    
    application_dependencies = ApplicationDependencies(
        health_router=health_router,
        clouds_router=clouds_router,
    )

    return create_dependencies_graph(config, application_dependencies)