from abc import abstractmethod
from typing import Optional

from sh_edraft.configuration.application_host import ApplicationHost
from sh_edraft.logging.model.log_settings import LoggingSettings
from sh_edraft.service.base.service_base import ServiceBase
from sh_edraft.time.model.time_format_settings import TimeFormatSettings


class LoggerBase(ServiceBase):

    @abstractmethod
    def __init__(self):
        ServiceBase.__init__(self)

        self._log_settings: Optional[LoggingSettings] = None
        self._time_format_settings: Optional[TimeFormatSettings] = None
        self._app_host: Optional[ApplicationHost] = None

    @abstractmethod
    def header(self, string: str): pass

    @abstractmethod
    def trace(self, name: str, message: str): pass

    @abstractmethod
    def debug(self, name: str, message: str): pass

    @abstractmethod
    def info(self, name: str, message: str): pass

    @abstractmethod
    def warn(self, name: str, message: str): pass

    @abstractmethod
    def error(self, name: str, message: str, ex: Exception = None): pass

    @abstractmethod
    def fatal(self, name: str, message: str, ex: Exception = None): pass
