import allure
import pytest
import requests

@allure.feature ('Test Ping')
@allure.story ("Test server unavailable")
def test_ping(api_client):
    status_code = api_client.ping()
    assert status_code == 201, f"Expected status code 201 but got: {status_code}"

@allure.feature("Test Ping")
@allure.story("Test server unavailability")
def test_ping_server_unavailable(api_client, mocker):
    mocker.patch.object(api_client.session, "get", side_effect=Exception("Server unavailable"))

    with pytest.raises(Exception, match="Server unavailable"):
        api_client.ping()

@allure.feature("Test Ping")
@allure.story("Test wrong HTTP method")
def test_ping_wrong_method(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 405
    mocker.patch.object(api_client.session, "get", return_value=mock_response)

    with pytest.raises(AssertionError, match="Expected status code 201 but got: 405"):
        api_client.ping()







