from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

from services.data_fetch import DataFetchServiceHttp
from services.db_client import create_db_client
from services.http_client import create_http_client
from services.render import RenderService
from services.storage import JsonFileStorageService
from services.analysis import AnalysisService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["config.yaml"])
    # db_client = providers.Singleton(create_db_client, db_filename=config.db.filename)
    http_client = providers.Singleton(create_http_client)
    storage_service = providers.Factory(
        JsonFileStorageService, filename=config.storage.filename
    )
    data_fetch_service = providers.Factory(
        DataFetchServiceHttp,
        http_client=http_client,
        storage_service=storage_service,
    )
    analysis_service = providers.Factory(
        AnalysisService, data_fetch_service=data_fetch_service
    )
    render_service = providers.Factory(
        RenderService,
        analysis_service=analysis_service,
    )

    # 1) http request to get data
    # 2) munge data into something useful
    # 3) display data into something readable
