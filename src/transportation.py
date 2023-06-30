import logging
import time

from datetime import datetime as dt

from src.mozio_api import Mozio

logger = logging.getLogger(__name__)


def _get_lowest_price(search_results):
    l = float(search_results[0]["total_price"]["total_price"]["value"])
    for r in search_results:
        price = r["total_price"]["total_price"]["value"]
        price = float(price)
        if price <= l:
            result_id = r["result_id"]
    return result_id


class Tranportation:
    def __init__(self) -> None:
        self.mozio = Mozio()
        self.started_at = None
        self.search_id = None
        self.result_id = None
        self.reservation_id = None
        self.canceled = False
        self.error = None
        self.ended_at = None

    def __str__(self) -> str:
        return f"""
            🕛 Started at: {self.started_at}
            🕛 Ended at: {self.ended_at}
            ⌛ Duration (seconds): {self._get_duration()}
            ❌ Error: {self.error}
            🔍 Search ID: {self.search_id}
            🔍 Result ID: {self.result_id}
            🔍 Reservation ID: {self.reservation_id}
        """

    def _get_duration(self):
        try:
            assert self.started_at
            assert self.ended_at
            return (self.ended_at - self.started_at).total_seconds()
        except Exception:
            return None

    def _post_search(self):
        if self.search_id is None:
            s = self.mozio.post_search()
            return s["search_id"]
        return self.search_id

    def _get_cheapest_trip_result(self):
        assert self.search_id
        s = self.mozio.get_search(self.search_id)
        if s and len(s["results"]) > 0 and s["results"][0].get("result_id"):
            return _get_lowest_price(s["results"])

    def _get_reservation_id(self, with_error):
        assert self.search_id
        assert self.result_id

        flight_number = f"{int(time.mktime(dt.now().timetuple()))}"
        if with_error:
            flight_number = None

        self.mozio.new_reservation(self.search_id, self.result_id, flight_number)

        res = self.mozio.search_reservation(self.search_id)
        return res.get("reservations")[0].get("id")

    def _cancel_reservation(self):
        assert self.reservation_id
        self.mozio.delete_reservation(self.reservation_id)
        return True

    def run_pipeline(self, with_error):
        self.started_at = dt.now()
        try:
            logger.info("Getting search_id 🔎")
            self.search_id = self._post_search()

            logger.info("Getting result_id 🔎")
            self.result_id = self._get_cheapest_trip_result()

            logger.info("Getting reservation_id 🔎")
            self.reservation_id = self._get_reservation_id(with_error)

            logger.info("Canceling reservation ❌")
            self.canceled = self._cancel_reservation()

            logger.info("Done! 🥳 \n")
        except Exception as e:
            self.error = e
            logger.error(f"Error 😞! {self.error} \n")
        finally:
            self.ended_at = dt.now()
