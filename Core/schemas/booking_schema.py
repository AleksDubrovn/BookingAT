BOOKING_SCHEMA = {
    "type": "object",
    "properties": {
        "firstname": {"type": "string"},
        "lastname": {"type": "string"},

        "totalprice": {"type": "number"},
        "depositpaid": {"type": "boolean"},
        "bookingdates": {
            "type": "object",
            "properties": {
                "checkin": {"type": "string"},
                "checkout": {"type": "string"},
            },
            "required": ["checkin", "checkout"]
        },
        "additionalneeds": {"type": "string"},
    },
    "required": [
        "firstname",
        "lastname",
        "totalprice",
        "depositpaid",
        "bookingdates",
    ],
}


CREATE_BOOKING_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["bookingid", "booking"],
    "additionalProperties": False,
    "properties": {
        "bookingid": {
            "type": "integer",
            "minimum": 1
        },
        "booking": {
            "type": "object",
            "required": [
                "firstname",
                "lastname",
                "totalprice",
                "depositpaid",
                "bookingdates"
            ],
            "additionalProperties": False,
            "properties": {
                "firstname": {
                    "type": "string",
                    "minLength": 1
                },
                "lastname": {
                    "type": "string",
                    "minLength": 1
                },
                "totalprice": {
                    "type": "integer",
                    "minimum": 0
                },
                "depositpaid": {
                    "type": "boolean"
                },
                "bookingdates": {
                    "type": "object",
                    "required": ["checkin", "checkout"],
                    "additionalProperties": False,
                    "properties": {
                        "checkin": {
                            "type": "string",
                            "format": "date"
                        },
                        "checkout": {
                            "type": "string",
                            "format": "date"
                        }
                    }
                },
                "additionalneeds": {
                    "type": "string",
                    "minLength": 1
                }
            }
        }
    }
}
