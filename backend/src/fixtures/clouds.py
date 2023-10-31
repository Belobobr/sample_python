import pytest
from typing import List

from external_services.clouds import AivenCloud

@pytest.fixture(name="azure_cloud")
def azure_cloud() -> AivenCloud:
    return AivenCloud(
        cloud_description="Azure",
        cloud_name="azure-south-africa-north",
        geo_latitude=-25,
        geo_longitude=28, 
        geo_region="africa", 
        provider="azure",
        provider_description="Microsoft Azure",
    )

@pytest.fixture(name="upcloud_cloud")
def upcloud_cloud() -> AivenCloud:
    return AivenCloud(
        cloud_description="Asia, Singapore - UpCloud: Singapore",
        cloud_name="upcloud-sg-sin",
        geo_latitude=1,
        geo_longitude=103, 
        geo_region="asia-pacific", 
        provider="upcloud",
        provider_description="UpCloud",
    )

@pytest.fixture(name="google_cloud")
def google_cloud() -> AivenCloud:
    return AivenCloud(
        cloud_description="Asia, Hong Kong - Google Cloud: Hong Kong",
        cloud_name="google-asia-east2",
        geo_latitude=22,
        geo_longitude=114, 
        geo_region="asia-pacific", 
        provider="google",
        provider_description="Google Cloud Platform",
    )

@pytest.fixture(name="do_cloud")
def do_cloud() -> AivenCloud:
    return AivenCloud(
        cloud_description="Asia, India - DigitalOcean: Bangalore",
        cloud_name="do-blr",
        geo_latitude=12,
        geo_longitude=77, 
        geo_region="asia-pacific", 
        provider="do",
        provider_description="DigitalOcean",
    )

@pytest.fixture(name="aws_cloud")
def aws_cloud() -> AivenCloud:
    return AivenCloud(
        cloud_description="Africa, South Africa - Amazon Web Services: Cape Town",
        cloud_name="aws-af-south-1",
        geo_latitude=-33,
        geo_longitude=18, 
        geo_region="africa", 
        provider="aws",
        provider_description="Amazon Web Services",
    )


@pytest.fixture(name="clouds")
def clouds(azure_cloud, upcloud_cloud, google_cloud, do_cloud, aws_cloud) -> List[AivenCloud]:
    # azure', 'upcloud', 'google', 'do', 'aws'
    return [
        azure_cloud,
        upcloud_cloud,
        google_cloud,
        do_cloud,
        aws_cloud,
    ]