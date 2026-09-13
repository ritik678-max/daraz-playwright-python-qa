import allure
import pytest

from jsonschema import validate

from utils.api_client import APIClient
from utils.schemas import POST_SCHEMA


BASE_API_URL = (
    "https://jsonplaceholder.typicode.com"
)


@pytest.fixture
def api_client():

    return APIClient(
        BASE_API_URL
    )


@allure.feature("API Testing")
@allure.story("Posts API")
@pytest.mark.api
def test_get_post(api_client):

    response = api_client.get(
        "/posts/1"
    )

    assert response.status_code == 200

    body = response.json()

    # Validate response schema
    validate(
        instance=body,
        schema=POST_SCHEMA
    )

    assert body["id"] == 1
    assert "title" in body
    assert "body" in body
    assert "userId" in body


@allure.feature("API Testing")
@allure.story("Posts API")
@pytest.mark.api
def test_create_post(api_client):

    payload = {
        "title": "QA Automation",
        "body": "Playwright API Test",
        "userId": 1
    }

    response = api_client.post(
        "/posts",
        payload
    )

    assert response.status_code == 201

    body = response.json()

    # Validate response schema
    validate(
        instance=body,
        schema=POST_SCHEMA
    )

    assert body["title"] == payload["title"]
    assert body["body"] == payload["body"]
    assert body["userId"] == payload["userId"]


@allure.feature("API Testing")
@allure.story("Posts API")
@pytest.mark.api
def test_update_post(api_client):

    payload = {
        "id": 1,
        "title": "Updated QA Automation",
        "body": "Updated API Test",
        "userId": 1
    }

    response = api_client.put(
        "/posts/1",
        payload
    )

    assert response.status_code == 200

    body = response.json()

    # Validate response schema
    validate(
        instance=body,
        schema=POST_SCHEMA
    )

    assert body["id"] == payload["id"]
    assert body["title"] == payload["title"]
    assert body["body"] == payload["body"]
    assert body["userId"] == payload["userId"]


@allure.feature("API Testing")
@allure.story("Posts API")
@pytest.mark.api
def test_delete_post(api_client):

    response = api_client.delete(
        "/posts/1"
    )

    assert response.status_code == 200

    body = response.json()

    # JSONPlaceholder returns
    # an empty object for DELETE
    assert body == {}