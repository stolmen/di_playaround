from services.data_fetch import DataFetchServiceFake
from services.storage import MemoryStorageService
from .render import RenderService


def test_instantiation():
    service = RenderService(
        storage_service=MemoryStorageService(),
        data_fetch_service=DataFetchServiceFake(),
    )
