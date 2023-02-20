import textwrap

from cpl_cli.abc.file_template_abc import FileTemplateABC


class DiscordBotProjectFileAppsettings(FileTemplateABC):
    def __init__(self, path: str):
        FileTemplateABC.__init__(self, "", path, "{}")
        self._name = "appsettings.json"

    def get_code(self) -> str:
        return textwrap.dedent(
            """\
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
          },
          
          "DiscordBotSettings": {
            "Token": "",
            "Prefix": "!bot "
          }
        }
        """
        )
