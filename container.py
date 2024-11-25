from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

from services.data_fetch import DataFetchService
from services.db_client import create_db_client
from services.http_client import create_http_client
from services.render import RenderService
from services.storage import JsonFileStorageService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["config.yaml"])
    # db_client = providers.Singleton(create_db_client, db_filename=config.db.filename)
    http_client = providers.Singleton(create_http_client)
    data_fetch_service = providers.Factory(DataFetchService, http_client=http_client)
    storage_service = providers.Factory(
        JsonFileStorageService, filename=config.storage.filename
    )
    render_service = providers.Factory(
        RenderService,
        data_fetch_service=data_fetch_service,
        storage_service=storage_service,
    )
