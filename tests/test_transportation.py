import json
import os

from unittest import TestCase, mock

from src.transportation import Tranportation
from src.settings import DUMP_MOZIO_URL, DUMP_AUTH_TOKEN


MOCK_PATH = "tests/mocks/{file_name}"


def get_search_response():
    f = "search_response.json"
    with open(MOCK_PATH.format(file_name=f)) as f:
        return json.load(f)


def get_reservation_response():
    f = "reservation_response.json"
    with open(MOCK_PATH.format(file_name=f)) as f:
        return json.load(f)


@mock.patch.dict(
    os.environ, {"MOZIO_URL": DUMP_MOZIO_URL, "MOZIO_AUTH_TOKEN": DUMP_AUTH_TOKEN}
)
class TestMozioAPI(TestCase):
    @mock.patch("src.mozio_api.Mozio.delete_reservation")
    @mock.patch("src.mozio_api.Mozio.search_reservation")
    @mock.patch("src.mozio_api.Mozio.new_reservation")
    @mock.patch("src.mozio_api.Mozio.get_search")
    @mock.patch("src.mozio_api.Mozio.post_search")
    def test_successfull_pipline_flow(
        self,
        mock_post_search,
        mock_get_search,
        mock_new_reservation,
        mock_search_reservation,
        mock_delete_reservation,
    ):
        search_id = "ABC-123"
        result_id = "RES-3"
        reservation_id = "BLADI-1"

        mock_post_search.return_value = {"search_id": search_id}
        mock_get_search.return_value = get_search_response()
        mock_search_reservation.return_value = get_reservation_response()

        t = Tranportation()
        t.run_pipeline(False)

        self.assertEqual(t.search_id, search_id)
        self.assertEqual(t.result_id, result_id)
        self.assertEqual(t.reservation_id, reservation_id)
        self.assertIsNone(t.error)

    @mock.patch("src.mozio_api.Mozio.post_search")
    def test_failed_pipline_flow(self, mock_post_search):
        mock_post_search.return_value = {}

        t = Tranportation()
        t.run_pipeline(True)

        self.assertIsNotNone(t.error)
