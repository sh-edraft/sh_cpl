import textwrap

from cpl_cli._templates.template_file_abc import TemplateFileABC


class AppsettingsTemplate(TemplateFileABC):

    def __init__(self):
        TemplateFileABC.__init__(self)

        self._name = 'appsettings.json'
        self._path = ''
        self._value = textwrap.dedent("""\
        {
          "TimeFormatSettings": {
            "DateFormat": "%Y-%m-%d",
            "TimeFormat": "%H:%M:%S",
            "DateTimeFormat": "%Y-%m-%d %H:%M:%S.%f",
            "DateTimeLogFormat": "%Y-%m-%d_%H-%M-%S"
          },
        
          "LoggingSettings": {
            "Path": "logs/",
            "Filename": "log_$start_time.log",
            "ConsoleLogLevel": "ERROR",
            "FileLogLevel": "WARN"
          }
        }
        """)

    @property
    def name(self) -> str:
        return self._name

    @property
    def path(self) -> str:
        return self._path

    @property
    def value(self) -> str:
        return self._value
