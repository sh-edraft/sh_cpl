from collections import Callable

from sh_edraft.configuration.base.configuration_model_base import ConfigurationModelBase
from sh_edraft.configuration.base.configuration_base import ConfigurationBase


class Configuration(ConfigurationBase):

    def __init__(self):
        super().__init__()

        self._config: dict[type, object] = {}

    @property
    def config(self):
        return self._config

    def create(self): pass

    def add_config_by_type(self, key_type: type, value: object):
        self._config[key_type] = value

    def get_config_by_type(self, search_type: type) -> Callable[ConfigurationModelBase]:
        if search_type not in self._config:
            raise Exception(f'Config model by type {search_type} not found')

        for config_model in self._config:
            if config_model == search_type:
                return self._config[config_model]
