import os
import requests.models

from http import HTTPStatus
from unittest import TestCase, mock

from src.mozio_api import Mozio, notFound
from src.settings import DUMP_MOZIO_URL, DUMP_AUTH_TOKEN


def mocked_requests_get_404(*args, **kwargs):
    resp = requests.Response()
    resp.status_code = HTTPStatus.NOT_FOUND
    return resp


def mocked_requests_post_500(*args, **kwargs):
    resp = requests.Response()
    resp.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return resp


def mocked_requests_post_201(*args, **kwargs):
    resp = requests.Response()
    resp.status_code = HTTPStatus.CREATED
    resp.json = lambda: {"search_id": "123"}
    return resp


@mock.patch.dict(
    os.environ, {"MOZIO_URL": DUMP_MOZIO_URL, "MOZIO_AUTH_TOKEN": DUMP_AUTH_TOKEN}
)
class TestMozioAPI(TestCase):
    def test_env_variables_failure(self):
        del os.environ["MOZIO_URL"]

        with self.assertRaises(KeyError) as context:
            m = Mozio()
        self.assertEqual(str(context.exception), str(KeyError("MOZIO_URL")))
        self.assertTrue("MOZIO_URL" in str(context.exception))

    def test_env_variables_successfully(self):
        m = Mozio()
        self.assertEqual(m.URL, DUMP_MOZIO_URL)
        self.assertEqual(m.HEADERS["Api-Key"], DUMP_AUTH_TOKEN)

    @mock.patch("src.mozio_api.requests.get", side_effect=mocked_requests_get_404)
    def test_get_request_404_error(self, mock_get_request):
        search_id = "random-search-id"

        m = Mozio()
        r = m.get_search(search_id)

        self.assertTrue(r["response"], notFound)

        endpoint = m.ENDPOINTS["get_search"].format(search_id=search_id)
        mock_get_request.assert_called_with(
            url=f"{DUMP_MOZIO_URL}{endpoint}",
            headers={"Api-Key": DUMP_AUTH_TOKEN},
            params=None,
        )

    @mock.patch("src.mozio_api.requests.post", side_effect=mocked_requests_post_201)
    def test_post_request_successfully(self, mock_post_request):
        m = Mozio()
        r = m.post_search()

        self.assertTrue(r["search_id"], "123")

        endpoint = m.ENDPOINTS["post_search"]
        mock_post_request.assert_called_with(
            url=f"{DUMP_MOZIO_URL}{endpoint}",
            headers={"Api-Key": DUMP_AUTH_TOKEN},
            json=mock.ANY,
        )
