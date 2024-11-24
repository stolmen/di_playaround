from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

from services import (
    create_db_client,
    create_http_client,
    DataService,
    JsonFileStorageService,
)


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["config.yaml"])
    # db_client = providers.Singleton(create_db_client, db_filename=config.db.filename)
    http_client = providers.Singleton(create_http_client)
    storage_service = providers.Factory(
        JsonFileStorageService, filename=config.storage.filename
    )
    data_service = providers.Factory(
        DataService,
        # db_client=db_client,
        http_client=http_client,
        storage_service=storage_service,
    )
