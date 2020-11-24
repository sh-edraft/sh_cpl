import os
import shutil
import unittest
from datetime import datetime
from string import Template

from sh_edraft.configuration import ApplicationHost
from sh_edraft.logging import Logger
from sh_edraft.logging.base import LoggerBase
from sh_edraft.logging.model import LoggingSettings
from sh_edraft.time.model import TimeFormatSettings


class LoggerTest(unittest.TestCase):

    def setUp(self):
        self._app_host = ApplicationHost()
        self._services = self._app_host.services
        self._services.init(())
        self._services.create()

        self._log_settings = LoggingSettings()
        self._log_settings.from_dict({
            "Path": "logs/",
            "Filename": "log_$start_time.log",
            "ConsoleLogLevel": "TRACE",
            "FileLogLevel": "TRACE"
        })

        self._time_format_settings = TimeFormatSettings()
        self._time_format_settings.from_dict({
            "DateFormat": "%Y-%m-%d",
            "TimeFormat": "%H:%M:%S",
            "DateTimeFormat": "%Y-%m-%d %H:%M:%S.%f",
            "DateTimeLogFormat": "%Y-%m-%d_%H-%M-%S"
        })

        self._services.add_singleton(Logger, self._log_settings, self._time_format_settings, self._app_host)

    def tearDown(self):
        if os.path.isdir(self._log_settings.path):
            shutil.rmtree(self._log_settings.path)

    def _check_general_requirements(self):
        self.assertIsNotNone(self._services)
        self.assertIsNotNone(self._log_settings)
        self.assertIsNotNone(self._time_format_settings)

    def test_create(self):
        print(f'{__name__}.test_create:')
        logger: Logger = self._services.get_service(LoggerBase)
        self.assertIsNotNone(logger)

        logger.create()
        self.assertTrue(os.path.isdir(self._log_settings.path))

        log_file = Template(self._log_settings.filename).substitute(
            date_time_now=self._app_host.date_time_now.strftime(self._time_format_settings.date_time_format),
            start_time=self._app_host.start_time.strftime(self._time_format_settings.date_time_log_format)
        )
        self.assertTrue(os.path.isfile(self._log_settings.path + log_file))

    def test_header(self):
        print(f'{__name__}.test_header:')
        logger: Logger = self._services.get_service(LoggerBase)
        logger.create()
        logger.header('HeaderTest:')

        log_file = Template(self._log_settings.filename).substitute(
            date_time_now=self._app_host.date_time_now.strftime(self._time_format_settings.date_time_format),
            start_time=self._app_host.start_time.strftime(self._time_format_settings.date_time_log_format)
        )
        log_content = []

        try:
            with open(self._log_settings.path + log_file, "r") as log:
                log_content = log.readlines()
                log.close()
        except Exception as e:
            print('Cannot open log file', e)

        self.assertGreater(len(log_content), 0)
        self.assertEqual(log_content[len(log_content) - 1], 'HeaderTest:\n')

    def test_trace(self):
        print(f'{__name__}.test_trace:')
        logger: Logger = self._services.get_service(LoggerBase)
        logger.create()
        logger.trace(__name__, f'{__name__}.test_trace:')

        log_file = Template(self._log_settings.filename).substitute(
            date_time_now=self._app_host.date_time_now.strftime(self._time_format_settings.date_time_format),
            start_time=self._app_host.start_time.strftime(self._time_format_settings.date_time_log_format)
        )
        log_content = []

        try:
            with open(self._log_settings.path + log_file, "r") as log:
                log_content = log.readlines()
                log.close()
        except Exception as e:
            print('Cannot open log file', e)

        self.assertGreater(len(log_content), 0)
        self.assertTrue(log_content[len(log_content) - 1].endswith(f'[ TRACE ] [ {__name__} ]: {__name__}.test_trace:\n'))

    def test_debug(self):
        print(f'{__name__}.test_debug:')
        logger: Logger = self._services.get_service(LoggerBase)
        logger.create()
        logger.debug(__name__, f'{__name__}.test_debug:')

        log_file = Template(self._log_settings.filename).substitute(
            date_time_now=self._app_host.date_time_now.strftime(self._time_format_settings.date_time_format),
            start_time=self._app_host.start_time.strftime(self._time_format_settings.date_time_log_format)
        )
        log_content = []

        try:
            with open(self._log_settings.path + log_file, "r") as log:
                log_content = log.readlines()
                log.close()
        except Exception as e:
            print('Cannot open log file', e)

        self.assertGreater(len(log_content), 0)
        self.assertTrue(log_content[len(log_content) - 1].endswith(f'[ DEBUG ] [ {__name__} ]: {__name__}.test_debug:\n'))

    def test_info(self):
        print(f'{__name__}.test_info:')
        logger: Logger = self._services.get_service(LoggerBase)
        logger.create()
        logger.info(__name__, f'{__name__}.test_info:')

        log_file = Template(self._log_settings.filename).substitute(
            date_time_now=self._app_host.date_time_now.strftime(self._time_format_settings.date_time_format),
            start_time=self._app_host.start_time.strftime(self._time_format_settings.date_time_log_format)
        )
        log_content = []

        try:
            with open(self._log_settings.path + log_file, "r") as log:
                log_content = log.readlines()
                log.close()
        except Exception as e:
            print('Cannot open log file', e)

        self.assertGreater(len(log_content), 0)
        self.assertTrue(log_content[len(log_content) - 1].endswith(f'[ INFO ] [ {__name__} ]: {__name__}.test_info:\n'))

    def test_warn(self):
        print(f'{__name__}.test_warn:')
        logger: Logger = self._services.get_service(LoggerBase)
        logger.create()
        logger.warn(__name__, f'{__name__}.test_warn:')

        log_file = Template(self._log_settings.filename).substitute(
            date_time_now=self._app_host.date_time_now.strftime(self._time_format_settings.date_time_format),
            start_time=self._app_host.start_time.strftime(self._time_format_settings.date_time_log_format)
        )
        log_content = []

        try:
            with open(self._log_settings.path + log_file, "r") as log:
                log_content = log.readlines()
                log.close()
        except Exception as e:
            print('Cannot open log file', e)

        self.assertGreater(len(log_content), 0)
        self.assertTrue(log_content[len(log_content) - 1].endswith(f'[ WARN ] [ {__name__} ]: {__name__}.test_warn:\n'))

    def test_error(self):
        print(f'{__name__}.test_error:')
        logger: Logger = self._services.get_service(LoggerBase)
        logger.create()
        logger.error(__name__, f'{__name__}.test_error:')

        log_file = Template(self._log_settings.filename).substitute(
            date_time_now=self._app_host.date_time_now.strftime(self._time_format_settings.date_time_format),
            start_time=self._app_host.start_time.strftime(self._time_format_settings.date_time_log_format)
        )
        log_content = []

        try:
            with open(self._log_settings.path + log_file, "r") as log:
                log_content = log.readlines()
                log.close()
        except Exception as e:
            print('Cannot open log file', e)

        self.assertGreater(len(log_content), 0)
        self.assertTrue(log_content[len(log_content) - 1].endswith(f'[ ERROR ] [ {__name__} ]: {__name__}.test_error:\n'))

    def test_fatal(self):
        print(f'{__name__}.test_fatal:')
        logger: Logger = self._services.get_service(LoggerBase)
        logger.create()
        with self.assertRaises(SystemExit):
            logger.fatal(__name__, f'{__name__}.test_fatal:')

        log_file = Template(self._log_settings.filename).substitute(
            date_time_now=self._app_host.date_time_now.strftime(self._time_format_settings.date_time_format),
            start_time=self._app_host.start_time.strftime(self._time_format_settings.date_time_log_format)
        )
        log_content = []

        try:
            with open(self._log_settings.path + log_file, "r") as log:
                log_content = log.readlines()
                log.close()
        except Exception as e:
            print('Cannot open log file', e)

        self.assertGreater(len(log_content), 0)
        self.assertTrue(log_content[len(log_content) - 1].endswith(f'[ ERROR ] [ {__name__} ]: {__name__}.test_fatal:\n'))
