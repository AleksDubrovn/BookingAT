import allure
import jsonschema
import pytest
from pydantic import ValidationError as PydanticValidationError
from requests.exceptions import HTTPError

from Core.models.booking import BookingResponse
from Core.schemas.booking_schema import CREATE_BOOKING_RESPONSE_SCHEMA


@allure.feature("Test Booking")
@allure.suite("Positive: create Booking with custom data")
def test_create_booking_with_custom_data(api_client):
    booking_data = {
        "firstname": "Ivan",
        "lastname": "Ivanovich",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-02-01",
            "checkout": "2025-02-10"
        },
        "additionalneeds": "Dinner"
    }

    response = api_client.create_booking(booking_data)

    with allure.step("Проверка схемы ответа с помощью Pydantic"):
        try:
            BookingResponse.model_validate(response)
        except PydanticValidationError as error:
            raise AssertionError(
                f"Response validation failed: {error}"
            ) from error

    with allure.step("Validate response schema"):
        jsonschema.validate(
            instance=response,
            schema=CREATE_BOOKING_RESPONSE_SCHEMA,
            format_checker=jsonschema.FormatChecker(),
        )

    with allure.step("Check booking data"):
        assert response["booking"] == booking_data

@allure.suite("Negative: create booking without required field")
@pytest.mark.parametrize(
    "field",
    ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"]
)
def test_create_booking_without_required_field(api_client, generate_random_booking_data, field):
    with allure.step("Data preparation"):
        booking_data = generate_random_booking_data.copy()
        booking_data.pop(field)
    with allure.step(f"send request without {field}"):
        with pytest.raises(HTTPError) as error:
            api_client.create_booking(booking_data)
        response = error.value.response
        with allure.step("Assert status code is 500"):
            assert response.status_code == 500, (
                f"Expected status code 500, but got {response.status_code}"
            )


@pytest.mark.parametrize("firstname", [123, True, None, {}, []])
def test_create_booking_with_invalid_firstname(api_client, generate_random_booking_data, firstname):
    with allure.step("Data preparation"):
        booking_data = generate_random_booking_data.copy()
        booking_data["firstname"] = firstname

    with pytest.raises(HTTPError) as error:
        api_client.create_booking(booking_data)
    response = error.value.response
    with allure.step("Assert status code is 500"):
        assert response.status_code == 500, (
            f"Expected status code 500, but got {response.status_code}"
        )
