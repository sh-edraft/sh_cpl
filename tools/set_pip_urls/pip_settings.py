import traceback

from cpl_core.environment.environment_name_enum import EnvironmentNameEnum

from cpl_core.configuration.configuration_model_abc import ConfigurationModelABC
from cpl_core.console import Console


class PIPSettings(ConfigurationModelABC):

    def __init__(self):
        ConfigurationModelABC.__init__(self)

        self._production = ''
        self._staging = ''
        self._development = ''

    @property
    def production(self):
        return self._production

    @property
    def staging(self):
        return self._staging

    @property
    def development(self):
        return self._development

    def from_dict(self, settings: dict):
        try:
            self._production = settings[EnvironmentNameEnum.production.value]
            self._staging = settings[EnvironmentNameEnum.staging.value]
            self._development = settings[EnvironmentNameEnum.development.value]
        except Exception as e:
            Console.error(f'[ ERROR ] [ {__name__} ]: Reading error in {self.__name__} settings')
            Console.error(f'[ EXCEPTION ] [ {__name__} ]: {e} -> {traceback.format_exc()}')
