import datetime
import os
import traceback
from string import Template
from typing import Optional

from sh_edraft.logging.base.logger_base import LoggerBase
from sh_edraft.logging.model.log_level import LoggingLevel
from sh_edraft.utils.console import Console


class Logger(LoggerBase):

    def __init__(self):
        LoggerBase.__init__(self)

        self._log: Optional[str] = None
        self._path: Optional[str] = None
        self._level: Optional[LoggingLevel] = None
        self._console: Optional[LoggingLevel] = None

    def init(self, args: tuple):
        self._log_settings = args[0]
        self._time_format_settings = args[1]
        self._app_host = args[2]

        self._log = Template(self._log_settings.filename).substitute(
            date_time_now=self._app_host.date_time_now.strftime(self._time_format_settings.date_time_format),
            start_time=self._app_host.start_time.strftime(self._time_format_settings.date_time_log_format)
        )
        self._path = self._log_settings.path
        self._level = self._log_settings.level
        self._console = self._log_settings.console

    def _get_datetime_now(self) -> str:
        try:
            return datetime.datetime.now().strftime(self._time_format_settings.date_time_format)
        except Exception as e:
            self.error(__name__, 'Cannot get time', ex=e)

    def _get_date(self) -> str:
        try:
            return datetime.datetime.now().strftime(self._time_format_settings.date_format)
        except Exception as e:
            self.error(__name__, 'Cannot get date', ex=e)

    def create(self) -> None:
        """ path """
        try:
            # check if log file path exists
            if not os.path.exists(self._path):
                os.mkdir(self._path)
        except Exception as e:
            self.fatal(__name__, 'Cannot create log dir', ex=e)

        """ create new log file """
        try:
            # open log file, create if not exists
            path = f'{self._path}{self._log}'
            f = open(path, "w+")
            Console.write_line(f'[{__name__}]: Using log file: {path}')
            f.close()
        except Exception as e:
            self.fatal(__name__, 'Cannot open log file', ex=e)

    def _append_log(self, string):
        try:
            # open log file and append always
            with open(self._path + self._log, "a+", encoding="utf-8") as f:
                f.write(string + '\n')
                f.close()
        except Exception as e:
            self.error(__name__, f'Cannot append log file, message: {string}', ex=e)

    def _get_string(self, name: str, level: LoggingLevel, message: str) -> str:
        log_level = level.name
        return f'<{self._get_datetime_now()}> [ {log_level} ] [ {name} ]: {message}'

    def header(self, string: str):
        # append log and print message
        self._append_log(string)
        Console.write_line(string, 'white')

    def trace(self, name: str, message: str):
        output = self._get_string(name, LoggingLevel.TRACE, message)

        # check if message can be written to log
        if self._level.value >= LoggingLevel.TRACE.value:
            self._append_log(output)

        # check if message can be shown in console
        if self._console.value >= LoggingLevel.TRACE.value:
            Console.write_line(output, 'green')

    def debug(self, name: str, message: str):
        output = self._get_string(name, LoggingLevel.DEBUG, message)

        # check if message can be written to log
        if self._level.value >= LoggingLevel.DEBUG.value:
            self._append_log(output)

        # check if message can be shown in console
        if self._console.value >= LoggingLevel.DEBUG.value:
            Console.write_line(output, 'green')

    def info(self, name: str, message: str):
        output = self._get_string(name, LoggingLevel.INFO, message)

        # check if message can be written to log
        if self._level.value >= LoggingLevel.INFO.value:
            self._append_log(output)

        # check if message can be shown in console
        if self._console.value >= LoggingLevel.INFO.value:
            Console.write_line(output, 'green')

    def warn(self, name: str, message: str):
        output = self._get_string(name, LoggingLevel.WARN, message)

        # check if message can be written to log
        if self._level.value >= LoggingLevel.WARN.value:
            self._append_log(output)

        # check if message can be shown in console
        if self._console.value >= LoggingLevel.WARN.value:
            Console.write_line(output, 'yellow')

    def error(self, name: str, message: str, ex: Exception = None):
        output = ''
        if ex is not None:
            tb = traceback.format_exc()
            self.error(name, message)
            output = self._get_string(name, LoggingLevel.ERROR, f'{ex} -> {tb}')
        else:
            output = self._get_string(name, LoggingLevel.ERROR, message)

        # check if message can be written to log
        if self._level.value >= LoggingLevel.ERROR.value:
            self._append_log(output)

        # check if message can be shown in console
        if self._console.value >= LoggingLevel.ERROR.value:
            Console.write_line(output, 'red')

    def fatal(self, name: str, message: str, ex: Exception = None):
        output = ''
        if ex is not None:
            tb = traceback.format_exc()
            self.error(name, message)
            output = self._get_string(name, LoggingLevel.ERROR, f'{ex} -> {tb}')
        else:
            output = self._get_string(name, LoggingLevel.ERROR, message)

        # check if message can be written to log
        if self._level.value >= LoggingLevel.FATAL.value:
            self._append_log(output)

        # check if message can be shown in console
        if self._console.value >= LoggingLevel.FATAL.value:
            Console.write_line(output, 'red')

        exit()
