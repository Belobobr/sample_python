import http.client
import json
from typing import Dict, List
from unittest.mock import Mock, patch

import pydantic
import pytest
from api.payload import BodyClouds
from config import get_config
from dependencies import (ApplicationDependenciesGraph,
                          provide_dependencies_graph)
from entities.clouds import (Cloud, SearchCloudsFilter, SearchCloudsSort,
                             SearchClouds)
from fastapi.testclient import TestClient
from fixtures.clouds import (aws_cloud, azure_cloud, clouds, do_cloud,
                             google_cloud, upcloud_cloud)
from geo.geo import Point, get_distance_between_two_points
from server import create_application


@pytest.fixture
def clouds_body(clouds: List[Cloud]) -> BodyClouds:
    return BodyClouds(
        clouds=clouds
    )

@pytest.fixture
def mock_http_client_with_clouds(clouds_body):
    mock_response = Mock()
    mock_response.status = 200
    mock_response.read.return_value = json.dumps(clouds_body.dict()).encode()
    with patch.object(http.client.HTTPConnection, 'getresponse', return_value=mock_response):
        yield

@pytest.fixture(name="application_dependencies_graph")
def application_dependencies_graph() -> ApplicationDependenciesGraph:
    config = get_config()
    test_application_dependencies_graph = provide_dependencies_graph(config)
    return test_application_dependencies_graph


@pytest.fixture(name="client_with_fixed_clouds")
def client_with_fixed_clouds(application_dependencies_graph: ApplicationDependenciesGraph) -> TestClient:
    app = create_application(application_dependencies_graph)
    return TestClient(app)


@pytest.mark.usefixtures('mock_http_client_with_clouds')
def test_when_user_requests_clouds_without_filters_should_return_whole_list(
    client_with_fixed_clouds: TestClient, 
    clouds: List[Cloud]
):
    response = client_with_fixed_clouds.post(
        "/api/clouds:search", 
        json=SearchClouds().dict()
    )
    
    assert response.status_code == 200
    assert response.json() == BodyClouds(clouds=clouds).dict()


@pytest.mark.usefixtures('mock_http_client_with_clouds')
def test_when_user_requests_clouds_with_filter_by_provider_should_return_filtered_list(
    client_with_fixed_clouds: TestClient, 
    clouds: List[Cloud],
    upcloud_cloud: Cloud
):
    response = client_with_fixed_clouds.post(
        "/api/clouds:search", 
        json=SearchClouds(
            filter=SearchCloudsFilter(
                provider="upcloud"
            )
        ).dict()
    )
    
    assert response.status_code == 200
    assert response.json() == BodyClouds(
        clouds=[
            upcloud_cloud,
        ]
    ).dict()

@pytest.mark.usefixtures('mock_http_client_with_clouds')
def test_when_user_requests_clouds_with_sort_by_closest_to_user_should_return_sorted_list(
    client_with_fixed_clouds: TestClient, 
    clouds: List[Cloud],
):
    user_location = Point(
        latitude=2,
        longitude=103,
    )

    response = client_with_fixed_clouds.post(
        "/api/clouds:search", 
        json=SearchClouds(
            sort=SearchCloudsSort(
                user_geo_latitude=user_location.latitude,
                user_geo_longitude=user_location.longitude
            )
        ).dict()
    )
    
    assert response.status_code == 200

    clouds_sorted_by_closest_to_user = get_clouds_sorted_by_closest_to_user(user_location, clouds)

    assert response.json() == BodyClouds(
        clouds=clouds_sorted_by_closest_to_user
    ).dict()


def get_clouds_sorted_by_closest_to_user(user_point: Point, clouds: List[Cloud]) -> List[Cloud]:
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

