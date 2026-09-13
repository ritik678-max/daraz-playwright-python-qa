import requests
import allure
import pytest


BASE_API_URL = "https://jsonplaceholder.typicode.com"


@allure.feature("API Testing")
@allure.story("Users API")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.api
def test_get_users():

    with allure.step("Send GET request to users endpoint"):

        response = requests.get(
            f"{BASE_API_URL}/users",
            timeout=10
        )

    with allure.step("Verify status code"):

        assert response.status_code == 200

    with allure.step("Verify response contains users"):

        users = response.json()

        assert isinstance(users, list)
        assert len(users) > 0

    with allure.step("Verify first user structure"):

        first_user = users[0]

        assert "id" in first_user
        assert "name" in first_user
        assert "email" in first_user