import pytest
import pydantic
import requests
import json
from unittest.mock import MagicMock, Mock, patch
from fastapi.testclient import TestClient
from typing import List, Dict
import requests_mock
import http.client

from config import get_config
from server import create_application, provide_dependencies_graph
from dependencies import ApplicationDependenciesGraph
from external_api.clouds import AivenCloud, AivenClouds
from external_api.index import ExternalApi, Result
from routes.clouds import create_clouds_router, create_cloud_router_dependencies
from schemas.clouds import SearchCloudsResponse, SearchCloudsRequest, CloudRequestFilter, CloudRequestSort
from fixtures.clouds import clouds, azure_cloud, upcloud_cloud, google_cloud, do_cloud, aws_cloud
from geo.geo import Point, get_distance_between_two_points

# TODO tests using patch

# def requests_side_effect(*args):
#     vals = {(1, 2): 1, (2, 3): 2, (3, 4): 3}
#     return vals[args]

# def test_requests_with_side_effects():
#     mock = MagicMock(side_effect=requests_side_effect)
#     assert mock(1,2) == 1
#     assert mock(2,3) == 2
#     assert mock(3,4) == 3


# @patch("http.client.HTTPResponse")
# def requests_mock(*args, **kwargs):
#     # Implement the desired behavior of the mock here
#     response = http.client.HTTPResponse()
#     response.status = 200
#     response.read.return_value = {}
#     return response

# @patch.object(http.client.HTTPConnection, "request", requests_mock)
# def test_my_function():
#     conn = http.client.HTTPConnection("example.com")
#     conn.request("GET", "/")
#     response = conn.getresponse()
#     pass


# @patch("http.client.HTTPResponse")
# def requests_mock(*args, **kwargs):
#     # Implement the desired behavior of the mock here
#     response = http.client.HTTPResponse()
#     response.status = 200
#     response.read.return_value = {}
#     return response

# def test_my_function():
    # with patch.object(http.client.HTTPConnection, "getresponse", requests_mock):
        # conn = http.client.HTTPConnection("example.com")
        # conn.request("GET", "/")
        # response = conn.getresponse()
    #     pass

# @pytest.fixture
# def mock_response():
#     mock_response = MagicMock()
#     mock_response.status = 200
#     mock_response.read.return_value = b'{}'
#     return mock_response

# @pytest.fixture
# def mock_http_client(mock_response):
#     with patch.object(http.client.HTTPConnection, 'getresponse', return_value=mock_response):
#         yield

# @pytest.mark.usefixtures('mock_http_client')
# def test_my_function():
#     conn = http.client.HTTPConnection("example.com")
#     conn.request("GET", "/")
#     response = conn.getresponse()
#     assert response.status == 200

# @pytest.fixture
# def clouds_body(clouds: List[AivenCloud]) -> AivenClouds:
#     return AivenClouds(
#         clouds=clouds
#     )

# @pytest.fixture
# def mock_http_client_with_clouds(clouds_body):
#     mock_response = Mock()
#     mock_response.status = 200
#     mock_response.read.return_value = json.dumps(clouds_body.dict()).encode()
#     with patch.object(http.client.HTTPConnection, 'getresponse', return_value=mock_response):
#         yield

# @pytest.mark.usefixtures('mock_http_client_with_clouds')
# def test_my_function(clouds_body: AivenClouds):
#     conn = http.client.HTTPConnection("example.com")
#     conn.request("GET", "/")
#     response = conn.getresponse()
#     assert response.status == 200

#     response_body = json.loads(response.read().decode())
#     response_body_formatted = AivenClouds(
#         **response_body
#     )
#     assert response_body_formatted == clouds_body

@pytest.fixture
def clouds_body(clouds: List[AivenCloud]) -> AivenClouds:
    return AivenClouds(
        clouds=clouds
    )

@pytest.fixture
def mock_http_client_with_clouds(clouds_body):
    mock_response = Mock()
    mock_response.status = 200
    mock_response.read.return_value = json.dumps(clouds_body.dict()).encode()
    with patch.object(http.client.HTTPConnection, 'getresponse', return_value=mock_response):
        yield

# @pytest.mark.usefixtures('mock_http_client_with_clouds')
# def test_my_function(clouds_body: AivenClouds):
#     conn = http.client.HTTPConnection("example.com")
#     conn.request("GET", "/")
#     response = conn.getresponse()
#     assert response.status == 200

#     response_body = json.loads(response.read().decode())
#     response_body_formatted = AivenClouds(
#         **response_body
#     )
#     assert response_body_formatted == clouds_body


# @pytest.fixture(name="application_dependencies_graph")
# def application_dependencies_graph(clouds: List[AivenCloud]) -> ApplicationDependenciesGraph:
#     config = get_config()
#     test_application_dependencies_graph = provide_dependencies_graph(config)

#     # override clouds router
#     class MockExternalServices(ExternalApi):
#         def get_clouds(self) -> List[AivenCloud]:
#             return Result(
#                 status=200,
#                 body=AivenClouds(
#                     clouds=clouds
#                 )
#             )

#     clouds_router = create_clouds_router(
#         config, 
#         dependencies=create_cloud_router_dependencies(
#             config, 
#             external_services=MockExternalServices()
#         )
#     )
#     test_application_dependencies_graph.clouds_router = clouds_router
#     #

#     return test_application_dependencies_graph


# @pytest.fixture(name="application_dependencies_graph")
# def application_dependencies_graph(clouds: List[AivenCloud]) -> ApplicationDependenciesGraph:
#     config = get_config()
#     test_application_dependencies_graph = provide_dependencies_graph(config)

#     # override clouds router
#     class MockExternalServices(ExternalApi):
#         def get_clouds(self) -> List[AivenCloud]:
#             return Result(
#                 status=200,
#                 body=AivenClouds(
#                     clouds=clouds
#                 )
#             )

#     clouds_router = create_clouds_router(
#         config, 
#         dependencies=create_cloud_router_dependencies(
#             config, 
#             external_services=MockExternalServices()
#         )
#     )
#     test_application_dependencies_graph.clouds_router = clouds_router
#     #

#     return test_application_dependencies_graph

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
    clouds: List[AivenCloud]
):
    response = client_with_fixed_clouds.post(
        "/api/clouds:search", 
        json=SearchCloudsRequest().dict()
    )
    
    assert response.status_code == 200
    assert response.json() == SearchCloudsResponse(clouds=clouds).dict()


@pytest.mark.usefixtures('mock_http_client_with_clouds')
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


# caching options?
# - cache all clouds, compute distance on the fly
# - create tile map of the world, 
# compute distance between tiles once, 
# map clouds to tiles, 
# compute closest clouds for every tile,
# store closest clouds for every tile in cache

@pytest.mark.usefixtures('mock_http_client_with_clouds')
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

