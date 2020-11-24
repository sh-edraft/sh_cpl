from abc import abstractmethod
from typing import Optional

from sh_edraft.logging.base.logger_base import LoggerBase
from sh_edraft.publishing.model.template import Template
from sh_edraft.service.base.service_base import ServiceBase


class PublisherBase(ServiceBase):

    @abstractmethod
    def __init__(self):
        ServiceBase.__init__(self)

        self._logger: Optional[LoggerBase] = None
        self._source_path: Optional[str] = None
        self._dist_path: Optional[str] = None
        self._settings: Optional[list[Template]] = None

        self._included_files: list[str] = []
        self._excluded_files: list[str] = []

    @property
    @abstractmethod
    def source_path(self) -> str: pass

    @property
    @abstractmethod
    def dist_path(self) -> str: pass

    @abstractmethod
    def publish(self) -> str: pass
