from abc import abstractmethod
from collections import Callable

from sh_edraft.configuration.base.configuration_model_base import ConfigurationModelBase
from sh_edraft.service.base.service_base import ServiceBase


class ConfigurationBase(ServiceBase):

    @abstractmethod
    def __init__(self):
        ServiceBase.__init__(self)

    @property
    @abstractmethod
    def config(self) -> dict[type, object]: pass

    @abstractmethod
    def add_config_by_type(self, key_type: type, value: object): pass

    @abstractmethod
    def get_config_by_type(self, search_type: ConfigurationModelBase) -> Callable[ConfigurationModelBase]: pass
