import pytest
import pydantic
from fastapi.testclient import TestClient
from typing import List, ClassVar, Dict

from config import get_config
from server import create_application, provide_dependencies_graph
from dependencies import ApplicationDependenciesGraph, create_dependencies_graph
from external_services.clouds import AivenCloud, ExternalServices, Result, AivenClouds
from routes.clouds import create_clouds_router, create_cloud_router_dependencies
from schemas.clouds import SearchCloudsResponse, SearchCloudsRequest

# @pytest.fixture(name="client")
# def fixture_client():
#     config = get_config()
#     app = create_application(config)
#     return TestClient(app)

# azure', 'upcloud', 'google', 'do', 'aws'
@pytest.fixture(name="clouds")
def clouds() -> List[AivenCloud]:
    return [
        AivenCloud(
            cloud_description="Azure",
            cloud_name="azure-south-africa-north",
            geo_latitude=-25,
            geo_longitude=28, 
            geo_region="africa", 
            provider="azure",
            provider_description="Microsoft Azure",
        ),
        AivenCloud(
            cloud_description="Asia, Singapore - UpCloud: Singapore",
            cloud_name="upcloud-sg-sin",
            geo_latitude=1,
            geo_longitude=103, 
            geo_region="asia-pacific", 
            provider="upcloud",
            provider_description="UpCloud",
        ),
        AivenCloud(
            cloud_description="Asia, Hong Kong - Google Cloud: Hong Kong",
            cloud_name="google-asia-east2",
            geo_latitude=22,
            geo_longitude=114, 
            geo_region="asia-pacific", 
            provider="google",
            provider_description="Google Cloud Platform",
        ),
        AivenCloud(
            cloud_description="Asia, India - DigitalOcean: Bangalore",
            cloud_name="do-blr",
            geo_latitude=12,
            geo_longitude=77, 
            geo_region="asia-pacific", 
            provider="do",
            provider_description="DigitalOcean",
        ),
        AivenCloud(
            cloud_description="Africa, South Africa - Amazon Web Services: Cape Town",
            cloud_name="aws-af-south-1",
            geo_latitude=-33,
            geo_longitude=18, 
            geo_region="africa", 
            provider="aws",
            provider_description="Amazon Web Services",
        ),
    ]

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

def test_when_user_requests_clouds_without_filters_should_return_whole_list(client_with_fixed_clouds: TestClient, clouds: List[AivenCloud]):
    response = client_with_fixed_clouds.post(
        "/api/clouds:search", 
        json=SearchCloudsRequest().dict()
    )
    
    assert response.status_code == 200
    assert response.json() == SearchCloudsResponse(clouds=clouds).dict()
    # assert is_valid(response.json(), SearchCloudsResponse)


def test_when_user_requests_clouds_with_filter_by_provider_should_return_filtered_list(client_with_fixed_clouds: TestClient, clouds: List[AivenCloud]):
    response = client_with_fixed_clouds.post(
        "/api/clouds:search", 
        json=SearchCloudsRequest(
            filter=SearchCloudsRequest.Filter(
                cloud=SearchCloudsRequest.CloudFilter(
                    provider="upcloud"
                )
            )
        ).dict()
    )
    
    assert response.status_code == 200
    assert response.json() == SearchCloudsResponse(
        clouds=[
            AivenCloud(
                cloud_description="Asia, Singapore - UpCloud: Singapore",
                cloud_name="upcloud-sg-sin",
                geo_latitude=1,
                geo_longitude=103, 
                geo_region="asia-pacific", 
                provider="upcloud",
                provider_description="UpCloud",
            ),
        ]
    ).dict()
    # assert is_valid(response.json(), SearchCloudsResponse)


def is_valid(json_object: Dict, class_name: type[pydantic.BaseModel]):
    try:
        class_name(**json_object)
        return True
    except pydantic.ValidationError as exc:
        return False

