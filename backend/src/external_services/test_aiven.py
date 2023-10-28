from external_services.clouds import get_aiven_clouds

def test_aiven_clouds():
    response = get_aiven_clouds()
    
    assert response.status == 200
    assert response.body.errors == None
    assert len(response.body.clouds) > 0
#[cloud for cloud in response.body.clouds if cloud.provider == "aws"][0]

# def test_hello(client):
#     response = client.get("/api/hello")
#     assert response.status_code == 200
#     assert response.json() == {"message": "Hello world"}


