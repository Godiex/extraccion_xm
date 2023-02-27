import sys

from dependency_injector.wiring import (
    inject,
    Provide
)
from infrastructure.container import Container
from core.services.crom_processing_service import CromProcessingService


class ScriptMixin(object):
    
    @staticmethod
    def _wire_modules():
        container = Container()
        container.wire(modules=[sys.modules[__name__]])

    @inject
    def _process_crom(
        self,
        crom_processing_service: CromProcessingService = Provide[Container.crom_processing_service]
    ):
        crom_processing_service.get()
