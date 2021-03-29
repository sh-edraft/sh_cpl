import datetime
import os
import traceback
from string import Template

from cpl.console.console import Console
from cpl.console.foreground_color_enum import ForegroundColorEnum
from cpl.environment.application_environment_abc import ApplicationEnvironmentABC
from cpl.logging.logger_abc import LoggerABC
from cpl.logging.logging_level_enum import LoggingLevelEnum
from cpl.logging.logging_settings import LoggingSettings
from cpl.time.time_format_settings import TimeFormatSettings


class Logger(LoggerABC):

    def __init__(self, logging_settings: LoggingSettings, time_format: TimeFormatSettings, env: ApplicationEnvironmentABC):
        """
        Service for logging
        :param logging_settings:
        :param time_format:
        :param app_runtime:
        """
        LoggerABC.__init__(self)

        self._env = env
        self._log_settings: LoggingSettings = logging_settings
        self._time_format_settings: TimeFormatSettings = time_format

        self._log = Template(self._log_settings.filename).substitute(
            date_time_now=self._env.date_time_now.strftime(self._time_format_settings.date_time_format),
            start_time=self._env.start_time.strftime(self._time_format_settings.date_time_log_format)
        )
        self._path = self._log_settings.path
        self._level = self._log_settings.level
        self._console = self._log_settings.console

        self.create()

    def _get_datetime_now(self) -> str:
        """
        Returns the date and time by given format
        :return:
        """
        try:
            return datetime.datetime.now().strftime(self._time_format_settings.date_time_format)
        except Exception as e:
            self.error(__name__, 'Cannot get time', ex=e)

    def _get_date(self) -> str:
        """
        Returns the date by given format
        :return:
        """
        try:
            return datetime.datetime.now().strftime(self._time_format_settings.date_format)
        except Exception as e:
            self.error(__name__, 'Cannot get date', ex=e)

    def create(self) -> None:
        """
        Creates path tree and logfile
        :return:
        """

        """ path """
        try:
            # check if log file path exists
            if not os.path.exists(self._path):
                os.makedirs(self._path)
        except Exception as e:
            self._fatal_console(__name__, 'Cannot create log dir', ex=e)

        """ create new log file """
        try:
            # open log file, create if not exists
            path = f'{self._path}{self._log}'
            f = open(path, "w+")
            Console.write_line(f'[{__name__}]: Using log file: {path}')
            f.close()
        except Exception as e:
            self._fatal_console(__name__, 'Cannot open log file', ex=e)

    def _append_log(self, string):
        """
        Writes to logfile
        :param string:
        :return:
        """
        try:
            # open log file and append always
            if not os.path.isdir(self._path):
                self._fatal_console(__name__, 'Log directory not found')

            with open(self._path + self._log, "a+", encoding="utf-8") as f:
                f.write(string + '\n')
                f.close()
        except Exception as e:
            self._fatal_console(__name__, f'Cannot append log file, message: {string}', ex=e)

    def _get_string(self, name: str, level: LoggingLevelEnum, message: str) -> str:
        """
        Returns input as log entry format
        :param name:
        :param level:
        :param message:
        :return:
        """
        log_level = level.name
        return f'<{self._get_datetime_now()}> [ {log_level} ] [ {name} ]: {message}'

    def header(self, string: str):
        # append log and print message
        self._append_log(string)
        Console.set_foreground_color(ForegroundColorEnum.default)
        Console.write_line(string)
        Console.set_foreground_color(ForegroundColorEnum.default)

    def trace(self, name: str, message: str):
        output = self._get_string(name, LoggingLevelEnum.TRACE, message)

        # check if message can be written to log
        if self._level.value >= LoggingLevelEnum.TRACE.value:
            self._append_log(output)

        # check if message can be shown in console_old
        if self._console.value >= LoggingLevelEnum.TRACE.value:
            Console.set_foreground_color(ForegroundColorEnum.green)
            Console.write_line(output)
            Console.set_foreground_color(ForegroundColorEnum.default)

    def debug(self, name: str, message: str):
        output = self._get_string(name, LoggingLevelEnum.DEBUG, message)

        # check if message can be written to log
        if self._level.value >= LoggingLevelEnum.DEBUG.value:
            self._append_log(output)

        # check if message can be shown in console_old
        if self._console.value >= LoggingLevelEnum.DEBUG.value:
            Console.set_foreground_color(ForegroundColorEnum.green)
            Console.write_line(output)
            Console.set_foreground_color(ForegroundColorEnum.default)

    def info(self, name: str, message: str):
        output = self._get_string(name, LoggingLevelEnum.INFO, message)

        # check if message can be written to log
        if self._level.value >= LoggingLevelEnum.INFO.value:
            self._append_log(output)

        # check if message can be shown in console_old
        if self._console.value >= LoggingLevelEnum.INFO.value:
            Console.set_foreground_color(ForegroundColorEnum.green)
            Console.write_line(output)
            Console.set_foreground_color(ForegroundColorEnum.default)

    def warn(self, name: str, message: str):
        output = self._get_string(name, LoggingLevelEnum.WARN, message)

        # check if message can be written to log
        if self._level.value >= LoggingLevelEnum.WARN.value:
            self._append_log(output)

        # check if message can be shown in console_old
        if self._console.value >= LoggingLevelEnum.WARN.value:
            Console.set_foreground_color(ForegroundColorEnum.yellow)
            Console.write_line(output)
            Console.set_foreground_color(ForegroundColorEnum.default)

    def error(self, name: str, message: str, ex: Exception = None):
        output = ''
        if ex is not None:
            tb = traceback.format_exc()
            self.error(name, message)
            output = self._get_string(name, LoggingLevelEnum.ERROR, f'{ex} -> {tb}')
        else:
            output = self._get_string(name, LoggingLevelEnum.ERROR, message)

        # check if message can be written to log
        if self._level.value >= LoggingLevelEnum.ERROR.value:
            self._append_log(output)

        # check if message can be shown in console_old
        if self._console.value >= LoggingLevelEnum.ERROR.value:
            Console.set_foreground_color(ForegroundColorEnum.red)
            Console.write_line(output)
            Console.set_foreground_color(ForegroundColorEnum.default)

    def fatal(self, name: str, message: str, ex: Exception = None):
        output = ''
        if ex is not None:
            tb = traceback.format_exc()
            self.error(name, message)
            output = self._get_string(name, LoggingLevelEnum.FATAL, f'{ex} -> {tb}')
        else:
            output = self._get_string(name, LoggingLevelEnum.FATAL, message)

        # check if message can be written to log
        if self._level.value >= LoggingLevelEnum.FATAL.value:
            self._append_log(output)

        # check if message can be shown in console_old
        if self._console.value >= LoggingLevelEnum.FATAL.value:
            Console.set_foreground_color(ForegroundColorEnum.red)
            Console.write_line(output)
            Console.set_foreground_color(ForegroundColorEnum.default)

        exit()

    def _fatal_console(self, name: str, message: str, ex: Exception = None):
        """
        Writes an error to console only
        :param name:
        :param message:
        :param ex:
        :return:
        """
        output = ''
        if ex is not None:
            tb = traceback.format_exc()
            self.error(name, message)
            output = self._get_string(name, LoggingLevelEnum.ERROR, f'{ex} -> {tb}')
        else:
            output = self._get_string(name, LoggingLevelEnum.ERROR, message)

        # check if message can be shown in console_old
        if self._console.value >= LoggingLevelEnum.FATAL.value:
            Console.set_foreground_color(ForegroundColorEnum.red)
            Console.write_line(output)
            Console.set_foreground_color(ForegroundColorEnum.default)

        exit()
