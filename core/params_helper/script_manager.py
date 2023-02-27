from .script_mixin import ScriptMixin
from .params_to_execute import ParamsToExecuteScript

METHODS_TO_EXECUTE: dict = dict(
    crom="_process_crom"
)


class ScriptManager(ScriptMixin):

    def __init__(self, params_to_execute: list) -> None:
        self._wire_modules()
        self.params_to_execute: list = params_to_execute
        self._valid_params = [param.value for param in ParamsToExecuteScript]
        
    def _validate_params_options(self):
        for param in self.params_to_execute:
            if param not in self._valid_params:
                raise Exception(f'El parametro {param} no es permitido')
    
    def execute(self):
        self._validate_params_options()

        for param in self.params_to_execute:
            method_to_execute = getattr(self, METHODS_TO_EXECUTE.get(param))
            method_to_execute()
