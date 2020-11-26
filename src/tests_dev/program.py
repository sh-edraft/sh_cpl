from typing import Optional

from sh_edraft.configuration.base import ConfigurationBase
from sh_edraft.hosting import ApplicationHost
from sh_edraft.hosting.base import ApplicationBase
from sh_edraft.hosting.model import EnvironmentName
from sh_edraft.logging import Logger
from sh_edraft.logging.base import LoggerBase
from sh_edraft.logging.model import LoggingSettings
from sh_edraft.service.base import ServiceProviderBase
from sh_edraft.time.model import TimeFormatSettings


class Program(ApplicationBase):

    def __init__(self):
        ApplicationBase.__init__(self)

        self._app_host: Optional[ApplicationHost] = None

        self._services: Optional[ServiceProviderBase] = None
        self._configuration: Optional[ConfigurationBase] = None

    def create_application_host(self):
        self._app_host = ApplicationHost('CPL_DEV_Test')
        self._services = self._app_host.services
        self._configuration = self._app_host.configuration

        self._app_host.environment.name = EnvironmentName.development

    def create_configuration(self):
        self._configuration.create()

        log_settings = LoggingSettings()
        log_settings.from_dict({
            "Path": "logs/",
            "Filename": "log_$start_time.log",
            "ConsoleLogLevel": "TRACE",
            "FileLogLevel": "TRACE"
        })

        time_format_settings = TimeFormatSettings()
        time_format_settings.from_dict({
            "DateFormat": "%Y-%m-%d",
            "TimeFormat": "%H:%M:%S",
            "DateTimeFormat": "%Y-%m-%d %H:%M:%S.%f",
            "DateTimeLogFormat": "%Y-%m-%d_%H-%M-%S"
        })

        self._configuration.add_config_by_type(LoggingSettings, log_settings)
        self._configuration.add_config_by_type(TimeFormatSettings, time_format_settings)

    def create_services(self):
        self._services.create()
        self._services.add_singleton(LoggerBase, Logger)
        logger: Logger = self._services.get_service(LoggerBase)
        logger.create()
        logger.header(self._app_host.name)

    def main(self):
        print('RUN')
