# class DataFetchService:


class DataFetchService:
    """Fetches seat data"""

    def list_seats(self):
        raise NotImplementedError

    def get_detailed_seat_info(self, seat_id):
        raise NotImplementedError


class DataFetchServiceFake(DataFetchService):
    """Fetches some seat data"""

    def list_seats(self):
        return []

    def get_detailed_seat_info(self, seat_id):
        return {}


class DataFetchServiceHttp(DataFetchService):
    """Fetches seat data"""

    def __init__(self, http_client):
        self.http_client = http_client

    def list_seats(self):
        bulk_data_url = "http://www.childcarseats.com.au/api/v1/child_car_seats/filter_data/retrieve?_format=json"
        response = self.http_client.get(bulk_data_url)
        seats = response.json()["seats"]
        filtered = [i for i in seats if i["type_ids"] == ["7", "500"]]
        return filtered

    def get_detailed_seat_info(self, seat_id):
        fine_data_url = f"http://www.childcarseats.com.au/api/v1/child_car_seats/seat_extra/retrieve/{seat_id}"
        response = self.http_client.get(fine_data_url)
        return response.json()
