import os
from string import Template

from sh_edraft.configuration import ApplicationHost
from sh_edraft.logging.base.logger_base import LoggerBase
from sh_edraft.logging.logger import Logger
from sh_edraft.logging.model.log_settings import LoggingSettings
from sh_edraft.time.model.time_format_settings import TimeFormatSettings


class LoggerTest:

    @staticmethod
    def start(app_host: ApplicationHost):
        services = app_host.services

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

        services.add_singleton(Logger, log_settings, time_format_settings, app_host)
        logger: Logger = services.get_service(LoggerBase)

        if logger is None:
            raise Exception(f'{__name__}: Service is None')

        logger.create()
        logger.info(__name__, 'test')

        if not os.path.isdir(log_settings.path):
            raise Exception(f'{__name__}: Log path was not created')

        log_file = Template(log_settings.filename).substitute(
            date_time_now=app_host.date_time_now.strftime(time_format_settings.date_time_format),
            start_time=app_host.start_time.strftime(time_format_settings.date_time_log_format)
        )
        if not os.path.isfile(log_settings.path + log_file):
            raise Exception(f'{__name__}: Log file was not created')
