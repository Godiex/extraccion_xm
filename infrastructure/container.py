from dependency_injector import containers, providers
from .http_client_xm import HttpClientXm
from .file_repository import FileRepository
from core import CromProcessingService


class Container(containers.DeclarativeContainer):
    http_client_xm = providers.Singleton(HttpClientXm)
    file_repository = providers.Singleton(FileRepository)
    crom_processing_service = providers.Singleton(CromProcessingService, http_client_xm, file_repository)
