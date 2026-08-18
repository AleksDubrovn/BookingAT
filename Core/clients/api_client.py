import os

import allure
import jsonschema
import requests
from dotenv import load_dotenv

from Core.clients.endpoints import Endpoints
from Core.schemas.booking_schema import BOOKING_SCHEMA
from Core.settings.config import Users, Timeout
from Core.settings.environments import Environment

load_dotenv()


class APIClient:
    def __init__(self):
        environment_str = os.getenv("ENVIRONMENT")

        try:
            environment = Environment[environment_str]
        except (KeyError, TypeError):
            raise ValueError(
                f"Unsupported environment value: {environment_str}"
            ) from None

        self.base_url = self.get_base_url(environment)
        self.session = requests.Session()
        self.session.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def get_base_url(self, environment: Environment) -> str:
        if environment == Environment.TESTING:
            return os.getenv("TEST_BASE_URL")

        if environment == Environment.PROD:
            return os.getenv("PROD_BASE_URL")

        raise ValueError(
            f"Unsupported environment: {environment}"
        )

    def ping(self):
        with allure.step("Get ping"):
            url = f"{self.base_url}{Endpoints.PING_ENDPOINT.value}"
            response = self.session.get(url, timeout=Timeout.TIMEOUT.value)
            response.raise_for_status()

        with allure.step("Assert status code"):
            assert response.status_code == 201, f"Expected status code 201 but got: {response.status_code}"

        return response.status_code

    def auth(self):
        with allure.step("Getting authentication"):
            url = f"{self.base_url}{Endpoints.AUTH_ENDPOINT.value}"
            payload = {"username": Users.USERNAME.value, "password": Users.PASSWORD.value}
            response = self.session.post(url, json=payload, timeout=Timeout.TIMEOUT.value)
            response.raise_for_status()
        with allure.step("Assert status code"):
            assert response.status_code == 200, (
                f"Expected status code 200 but got: {response.status_code}"
            )
        token = response.json()["token"]
        with allure.step("Update headers"):
            self.session.headers.update({"Cookie": f"token={token}"})
        return token

    def get_booking_by_id(self, booking_id):
        with allure.step("Get booking by id"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}"
            response = self.session.get(url, timeout=Timeout.TIMEOUT.value)
            response.raise_for_status()

        with allure.step("Assert status code"):
            assert response.status_code == 200, f"Expected status code 200 but got: {response.status_code}"

        with allure.step("Validate response schema"):
            response_json = response.json()
            jsonschema.validate(instance=response_json, schema=BOOKING_SCHEMA)

        return response_json

    def create_booking(self, booking_data):
        with allure.step("Create booking"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}"
            response = self.session.post(url, json=booking_data, timeout=Timeout.TIMEOUT.value)
            response.raise_for_status()

        with allure.step("Checking status code"):
            assert response.status_code == 200, f"Expected status code 200 but got: {response.status_code}"

        return response.json()

    def get_booking_ids(self, params=None):
        with allure.step("Get bookings by IDs"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}"
            response = self.session.get(url, params=params, timeout=Timeout.TIMEOUT.value)
            response.raise_for_status()

        with allure.step("Checking status code"):
            assert response.status_code == 200, f"Expected status code 200 but got: {response.status_code}"

        return response.json()

    def delete_booking(self, booking_id):
        with allure.step("Delete booking"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}"
            response = self.session.delete(url, timeout=Timeout.TIMEOUT.value)
            response.raise_for_status()

        with allure.step("Checking status code"):
            assert response.status_code == 201, f"Expected status code 201 but got: {response.status_code}"

        return response.status_code

    def partial_update_booking_by_id(self, booking_id, booking_json):
        with allure.step("Partial update booking"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}"
            response = self.session.patch(url, json=booking_json, timeout=Timeout.TIMEOUT.value)
            response.raise_for_status()

        with allure.step("Checking status code"):
            assert response.status_code == 200, f"Expected status code 200 but got: {response.status_code}"

        with allure.step("Validate response schema"):
            response_json = response.json()
            jsonschema.validate(instance=response_json, schema=BOOKING_SCHEMA)

        return response_json

    def update_booking_by_id(self, booking_id, booking_json):
        with allure.step("Update booking by id"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}"
            response = self.session.put(url, json=booking_json, timeout=Timeout.TIMEOUT.value)
            response.raise_for_status()

        with allure.step("Assert status code"):
            assert response.status_code == 200, f"Expected status code 200 but got: {response.status_code}"

        with allure.step("Validate response schema"):
            response_json = response.json()
            jsonschema.validate(instance=response_json, schema=BOOKING_SCHEMA)

        return response_json

