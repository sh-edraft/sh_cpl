import datetime
import os
import sys
import traceback
from string import Template

from cpl_core.configuration.configuration_model_abc import ConfigurationModelABC
from cpl_core.console.console import Console
from cpl_core.console.foreground_color_enum import ForegroundColorEnum
from cpl_core.environment.application_environment_abc import ApplicationEnvironmentABC
from cpl_core.logging.logger_abc import LoggerABC
from cpl_core.logging.logging_level_enum import LoggingLevelEnum
from cpl_core.logging.logging_settings import LoggingSettings
from cpl_core.time.time_format_settings import TimeFormatSettings


class Logger(LoggerABC):
    r"""Service for logging

    Parameter
    ---------
        logging_settings: :class:`cpl_core.logging.logging_settings.LoggingSettings`
            Settings for the logger
        time_format: :class:`cpl_core.time.time_format_settings.TimeFormatSettings`
            Time format settings
        env: :class:`cpl_core.environment.application_environment_abc.ApplicationEnvironmentABC`
            Environment of the application
    """

    def __init__(self, logging_settings: LoggingSettings, time_format: TimeFormatSettings, env: ApplicationEnvironmentABC):
        LoggerABC.__init__(self)

        self._env = env
        self._log_settings: LoggingSettings = logging_settings
        self._time_format_settings: TimeFormatSettings = time_format

        self._check_for_settings(self._time_format_settings, TimeFormatSettings)
        self._check_for_settings(self._log_settings, LoggingSettings)

        self._level = self._log_settings.level
        self._console = self._log_settings.console

        self.create()

    @property
    def _log(self) -> str:
        return Template(self._log_settings.filename).substitute(
            date_time_now=self._env.date_time_now.strftime(self._time_format_settings.date_time_format),
            date_now=self._env.date_time_now.strftime(self._time_format_settings.date_format),
            time_now=self._env.date_time_now.strftime(self._time_format_settings.time_format),
            start_time=self._env.start_time.strftime(self._time_format_settings.date_time_log_format)
        )

    @property
    def _path(self) -> str:
        return Template(self._log_settings.path).substitute(
            date_time_now=self._env.date_time_now.strftime(self._time_format_settings.date_time_format),
            date_now=self._env.date_time_now.strftime(self._time_format_settings.date_format),
            time_now=self._env.date_time_now.strftime(self._time_format_settings.time_format),
            start_time=self._env.start_time.strftime(self._time_format_settings.date_time_log_format)
        )

    def _check_for_settings(self, settings: ConfigurationModelABC, settings_type: type):
        self._level = LoggingLevelEnum.OFF
        self._console = LoggingLevelEnum.FATAL
        if settings is None:
            self.fatal(__name__, f'Configuration for {settings_type} not found')

    def _get_datetime_now(self) -> str:
        r"""Returns the date and time by given format

        Returns
        -------
            Date and time in given format
        """
        try:
            return datetime.datetime.now().strftime(self._time_format_settings.date_time_format)
        except Exception as e:
            self.error(__name__, 'Cannot get time', ex=e)

    def _get_date(self) -> str:
        r"""Returns the date by given format

        Returns
        -------
            Date in given format
        """
        try:
            return datetime.datetime.now().strftime(self._time_format_settings.date_format)
        except Exception as e:
            self.error(__name__, 'Cannot get date', ex=e)

    def create(self) -> None:
        r"""Creates path tree and logfile"""

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
            permission = 'a+'
            if not os.path.isfile(path):
                permission = 'w+'

            f = open(path, permission)
            Console.write_line(f'[{__name__}]: Using log file: {path}')
            f.close()
        except Exception as e:
            self._fatal_console(__name__, 'Cannot open log file', ex=e)

    def _append_log(self, string: str):
        r"""Writes to logfile

        Parameter
        ---------
            string: :class:`str`
        """
        try:
            # open log file and append always
            if not os.path.isdir(self._path):
                self._warn_console(__name__, 'Log directory not found, try to recreate logger')
                self.create()

            with open(self._path + self._log, "a+", encoding="utf-8") as f:
                f.write(string + '\n')
                f.close()
        except Exception as e:
            self._fatal_console(__name__, f'Cannot append log file, message: {string}', ex=e)

    def _get_string(self, name: str, level: LoggingLevelEnum, message: str) -> str:
        r"""Returns input as log entry format

        Parameter
        ---------
            name: :class:`str`
                Name of the message
            level: :class:`cpl_core.logging.logging_level_enum.LoggingLevelEnum`
                Logging level
            message: :class:`str`
                Log message

        Returns
        -------
            Formatted string for logging
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

        # check if message can be shown in console
        if self._console.value >= LoggingLevelEnum.TRACE.value:
            Console.set_foreground_color(ForegroundColorEnum.green)
            Console.write_line(output)
            Console.set_foreground_color(ForegroundColorEnum.default)

    def debug(self, name: str, message: str):
        output = self._get_string(name, LoggingLevelEnum.DEBUG, message)

        # check if message can be written to log
        if self._level.value >= LoggingLevelEnum.DEBUG.value:
            self._append_log(output)

        # check if message can be shown in console
        if self._console.value >= LoggingLevelEnum.DEBUG.value:
            Console.set_foreground_color(ForegroundColorEnum.green)
            Console.write_line(output)
            Console.set_foreground_color(ForegroundColorEnum.default)

    def info(self, name: str, message: str):
        output = self._get_string(name, LoggingLevelEnum.INFO, message)

        # check if message can be written to log
        if self._level.value >= LoggingLevelEnum.INFO.value:
            self._append_log(output)

        # check if message can be shown in console
        if self._console.value >= LoggingLevelEnum.INFO.value:
            Console.set_foreground_color(ForegroundColorEnum.green)
            Console.write_line(output)
            Console.set_foreground_color(ForegroundColorEnum.default)

    def warn(self, name: str, message: str):
        output = self._get_string(name, LoggingLevelEnum.WARN, message)

        # check if message can be written to log
        if self._level.value >= LoggingLevelEnum.WARN.value:
            self._append_log(output)

        # check if message can be shown in console
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

        # check if message can be shown in console
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

        # check if message can be shown in console
        if self._console.value >= LoggingLevelEnum.FATAL.value:
            Console.set_foreground_color(ForegroundColorEnum.red)
            Console.write_line(output)
            Console.set_foreground_color(ForegroundColorEnum.default)

        sys.exit()

    def _warn_console(self, name: str, message: str):
        r"""Writes a warning to console only

        Parameter
        ---------
            name: :class:`str`
                Error name
            message: :class:`str`
                Error message
        """
        # check if message can be shown in console
        if self._console.value >= LoggingLevelEnum.WARN.value:
            Console.set_foreground_color(ForegroundColorEnum.yellow)
            Console.write_line(self._get_string(name, LoggingLevelEnum.WARN, message))
            Console.set_foreground_color(ForegroundColorEnum.default)

        sys.exit()

    def _fatal_console(self, name: str, message: str, ex: Exception = None):
        r"""Writes an error to console only

        Parameter
        ---------
            name: :class:`str`
                Error name
            message: :class:`str`
                Error message
            ex: :class:`Exception`
                Thrown exception
        """
        output = ''
        if ex is not None:
            tb = traceback.format_exc()
            self.error(name, message)
            output = self._get_string(name, LoggingLevelEnum.ERROR, f'{ex} -> {tb}')
        else:
            output = self._get_string(name, LoggingLevelEnum.ERROR, message)

        # check if message can be shown in console
        if self._console.value >= LoggingLevelEnum.FATAL.value:
            Console.set_foreground_color(ForegroundColorEnum.red)
            Console.write_line(output)
            Console.set_foreground_color(ForegroundColorEnum.default)

        sys.exit()
