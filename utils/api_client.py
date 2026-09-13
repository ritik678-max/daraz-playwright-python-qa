import json

import allure
import requests

from utils.logger import get_logger


logger = get_logger(__name__)


class APIClient:

    def __init__(self, base_url):

        self.base_url = base_url.rstrip("/")

        self.session = requests.Session()

        self.session.headers.update(
            {
                "Content-Type": "application/json"
            }
        )

    def _build_url(
        self,
        endpoint
    ):

        return (
            f"{self.base_url}/"
            f"{endpoint.lstrip('/')}"
        )

    def _attach_request(
        self,
        method,
        url,
        payload=None,
        params=None
    ):

        request_data = {
            "method": method,
            "url": url,
            "params": params,
            "payload": payload
        }

        allure.attach(
            json.dumps(
                request_data,
                indent=4
            ),
            name="API Request",
            attachment_type=
            allure.attachment_type.JSON
        )

        logger.info(
            f"API Request | "
            f"{method} | "
            f"{url}"
        )

        if params:

            logger.info(
                f"Query Params: "
                f"{params}"
            )

        if payload:

            logger.info(
                f"Request Payload: "
                f"{payload}"
            )

    def _attach_response(
        self,
        response
    ):

        try:

            response_body = (
                response.json()
            )

            response_text = json.dumps(
                response_body,
                indent=4
            )

        except ValueError:

            response_text = (
                response.text
            )

        response_data = {
            "status_code":
            response.status_code,

            "url":
            response.url,

            "body":
            response_body
            if "response_body" in locals()
            else response.text
        }

        allure.attach(
            json.dumps(
                response_data,
                indent=4
            ),
            name="API Response",
            attachment_type=
            allure.attachment_type.JSON
        )

        logger.info(
            f"API Response | "
            f"Status: "
            f"{response.status_code} | "
            f"{response.url}"
        )

        logger.info(
            f"Response Body: "
            f"{response_text}"
        )

    def get(
        self,
        endpoint,
        params=None
    ):

        url = self._build_url(
            endpoint
        )

        self._attach_request(
            method="GET",
            url=url,
            params=params
        )

        response = self.session.get(
            url,
            params=params,
            timeout=10
        )

        self._attach_response(
            response
        )

        return response

    def post(
        self,
        endpoint,
        payload
    ):

        url = self._build_url(
            endpoint
        )

        self._attach_request(
            method="POST",
            url=url,
            payload=payload
        )

        response = self.session.post(
            url,
            json=payload,
            timeout=10
        )

        self._attach_response(
            response
        )

        return response

    def put(
        self,
        endpoint,
        payload
    ):

        url = self._build_url(
            endpoint
        )

        self._attach_request(
            method="PUT",
            url=url,
            payload=payload
        )

        response = self.session.put(
            url,
            json=payload,
            timeout=10
        )

        self._attach_response(
            response
        )

        return response

    def delete(
        self,
        endpoint
    ):

        url = self._build_url(
            endpoint
        )

        self._attach_request(
            method="DELETE",
            url=url
        )

        response = (
            self.session.delete(
                url,
                timeout=10
            )
        )

        self._attach_response(
            response
        )

        return response