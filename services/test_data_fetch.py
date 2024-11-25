from .data_fetch import DataFetchServiceHttp
from .http_client import create_http_client


def test_instantiation():
    service = DataFetchServiceHttp(http_client=create_http_client())
