from dependency_injector import containers, providers
from .http_client_xm import HttpClientXm
from core import CromProcessingService


class Container(containers.DeclarativeContainer):
    http_client_xm = providers.Singleton(HttpClientXm)
    crom_processing_service = providers.Singleton(CromProcessingService, http_client_xm)
