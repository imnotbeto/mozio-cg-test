import time
import requests

from http import HTTPStatus
from requests.exceptions import HTTPError

from src.settings import GET_MOZIO_URL, GET_MOZIO_AUTH_TOKEN, MAX_POLLS


completedStatus = "completed"
notFound = "not found"


class Mozio:
    WAITING_TIME_SECS = 2
    POLL_COUNTER = 0
    MAX_POLLS = MAX_POLLS
    ENDPOINTS = {
        "post_search": "/v2/search/",
        "get_search": "/v2/search/{search_id}/poll/",
        "post_reservation": "/v2/reservations/",
        "search_reservation": "/v2/reservations/{search_id}/poll/",
        "delete_reservation": "/v2/reservations/{confirmation_number}",
    }

    def __init__(self) -> None:
        self.URL = GET_MOZIO_URL()
        self.HEADERS = {"Api-Key": GET_MOZIO_AUTH_TOKEN()}

    def _post(self, url, body=None):
        try:
            r = requests.post(url=url, headers=self.HEADERS, json=body)
            r.raise_for_status()
            return r.json()
        except HTTPError as e:
            raise HTTPError(r.text, e.response.status_code)

    def _get(self, url, params=None):
        try:
            r = requests.get(url=url, headers=self.HEADERS, params=params)
            r.raise_for_status()
            return r.json()
        except HTTPError as e:
            if e.response.status_code == HTTPStatus.NOT_FOUND:
                return {"response": notFound}

            raise HTTPError(r.text, e.response.status_code)

    def _delete(self, url):
        try:
            r = requests.delete(url=url, headers=self.HEADERS)
            r.raise_for_status()
            return r.json()
        except HTTPError as e:
            raise HTTPError(r.text, e.response.status_code)

    def post_search(self):
        url = f"{self.URL}{self.ENDPOINTS['post_search']}"

        body = {
            "start_address": "44 Tehama Street, San Francisco, CA, USA",
            "end_address": "SFO",
            "mode": "one_way",
            "pickup_datetime": "2023-12-01 15:30",
            "num_passengers": 2,
            "currency": "USD",
            "campaign": "CARLOS GUERRERO - 2",
        }

        return self._post(url, body)

    def get_search(self, search_id):
        endpoint = self.ENDPOINTS["get_search"].format(search_id=search_id)
        url = f"{self.URL}{endpoint}"
        c = 0
        more_coming = True

        r = {}
        while c < self.MAX_POLLS and more_coming:
            c += 1
            r = self._get(url)

            results = r.get("results")
            if type(results) == list and len(results) > 0:
                return r

            more_coming = r.get("more_coming")
            if more_coming:
                time.sleep(self.WAITING_TIME_SECS)

        return r

    def new_reservation(self, search_id, result_id, flight_number):
        url = f"{self.URL}{self.ENDPOINTS['post_reservation']}"

        body = {
            "result_id": result_id,
            "search_id": search_id,
            "provider": {"property1": "Dummy External Provider"},
            "email": "carlos_guerrero@test.com",
            "phone_number": "+52-4441655778",
            "first_name": "Carlos",
            "last_name": "Guerrero",
            "airline": "2D",
            "flight_number": flight_number,
        }

        return self._post(url, body)

    def search_reservation(self, search_id):
        endpoint = self.ENDPOINTS["search_reservation"].format(search_id=search_id)
        url = f"{self.URL}{endpoint}"
        c = 0
        status_completed = False
        while c < self.MAX_POLLS and not status_completed:
            c += 1
            r = self._get(url)
            status_completed = r.get("status") == completedStatus
            if status_completed:
                return r
            time.sleep(self.WAITING_TIME_SECS)

    def delete_reservation(self, confirmation_number):
        endpoint = self.ENDPOINTS["delete_reservation"].format(
            confirmation_number=confirmation_number
        )
        url = f"{self.URL}{endpoint}"

        return self._delete(url)
