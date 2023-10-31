import pytest
import pydantic
from fastapi.testclient import TestClient
from typing import List, Dict

from config import get_config
from server import create_application, provide_dependencies_graph
from dependencies import ApplicationDependenciesGraph
from external_services.clouds import AivenCloud, ExternalServices, Result, AivenClouds
from routes.clouds import create_clouds_router, create_cloud_router_dependencies
from schemas.clouds import SearchCloudsResponse, SearchCloudsRequest, CloudRequestFilter, CloudRequestSort
from fixtures.clouds import clouds, azure_cloud, upcloud_cloud, google_cloud, do_cloud, aws_cloud
from geo.geo import Point, get_distance_between_two_points

@pytest.fixture(name="application_dependencies_graph")
def application_dependencies_graph(clouds: List[AivenCloud]) -> ApplicationDependenciesGraph:
    config = get_config()
    test_application_dependencies_graph = provide_dependencies_graph(config)

    # override clouds router
    class MockExternalServices(ExternalServices):
        def get_clouds(self) -> List[AivenCloud]:
            return Result(
                status=200,
                body=AivenClouds(
                    clouds=clouds
                )
            )

    clouds_router = create_clouds_router(
        config, 
        dependencies=create_cloud_router_dependencies(
            config, 
            external_services=MockExternalServices()
        )
    )
    test_application_dependencies_graph.clouds_router = clouds_router
    #

    return test_application_dependencies_graph

@pytest.fixture(name="client_with_fixed_clouds")
def client_with_fixed_clouds(application_dependencies_graph: ApplicationDependenciesGraph) -> TestClient:
    app = create_application(application_dependencies_graph)
    return TestClient(app)


def test_when_user_requests_clouds_without_filters_should_return_whole_list(
    client_with_fixed_clouds: TestClient, 
    clouds: List[AivenCloud]
):
    response = client_with_fixed_clouds.post(
        "/api/clouds:search", 
        json=SearchCloudsRequest().dict()
    )
    
    assert response.status_code == 200
    assert response.json() == SearchCloudsResponse(clouds=clouds).dict()


def test_when_user_requests_clouds_with_filter_by_provider_should_return_filtered_list(
    client_with_fixed_clouds: TestClient, 
    clouds: List[AivenCloud],
    upcloud_cloud: AivenCloud
):
    response = client_with_fixed_clouds.post(
        "/api/clouds:search", 
        json=SearchCloudsRequest(
            filter=CloudRequestFilter(
                provider="upcloud"
            )
        ).dict()
    )
    
    assert response.status_code == 200
    assert response.json() == SearchCloudsResponse(
        clouds=[
            upcloud_cloud,
        ]
    ).dict()


def test_when_user_requests_clouds_with_sort_by_closest_to_user_should_return_sorted_list(
    client_with_fixed_clouds: TestClient, 
    clouds: List[AivenCloud],
):
    user_location = Point(
        latitude=2,
        longitude=103,
    )

    response = client_with_fixed_clouds.post(
        "/api/clouds:search", 
        json=SearchCloudsRequest(
            sort=CloudRequestSort(
                user_geo_latitude=user_location.latitude,
                user_geo_longitude=user_location.longitude
            )
        ).dict()
    )
    
    assert response.status_code == 200

    clouds_sorted_by_closest_to_user = get_clouds_sorted_by_closest_to_user(user_location, clouds)

    assert response.json() == SearchCloudsResponse(
        clouds=clouds_sorted_by_closest_to_user
    ).dict()


def get_clouds_sorted_by_closest_to_user(user_point: Point, clouds: List[AivenCloud]) -> List[AivenCloud]:
    return sorted(
        clouds,
        key=lambda cloud: get_distance_between_two_points(
            user_point,
            cloud.as_point()
        )
    )

def is_valid(json_object: Dict, class_name: type[pydantic.BaseModel]):
    try:
        class_name(**json_object)
        return True
    except pydantic.ValidationError as exc:
        return False

