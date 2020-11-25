from abc import abstractmethod

from sh_edraft.logging.base.logger_base import LoggerBase
from sh_edraft.publishing.model.publish_settings_model import PublishSettingsModel
from sh_edraft.service.base.service_base import ServiceBase


class PublisherBase(ServiceBase):

    @abstractmethod
    def __init__(self, logger: LoggerBase, publish_settings: PublishSettingsModel):
        ServiceBase.__init__(self)

        self._logger: LoggerBase = logger
        self._publish_settings: PublishSettingsModel = publish_settings

    @property
    @abstractmethod
    def source_path(self) -> str: pass

    @property
    @abstractmethod
    def dist_path(self) -> str: pass

    @abstractmethod
    def include(self, path: str): pass

    @abstractmethod
    def exclude(self, path: str): pass

    @abstractmethod
    def publish(self) -> str: pass
