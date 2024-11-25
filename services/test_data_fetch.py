from .data_fetch import DataFetchService
from .http_client import create_http_client


def test_instantiation():
    service = DataFetchService(http_client=create_http_client())
