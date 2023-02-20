import json

from cpl_cli.abc.file_template_abc import FileTemplateABC


class DiscordBotProjectFile(FileTemplateABC):
    def __init__(self, name: str, path: str, code: dict):
        FileTemplateABC.__init__(self, "", path, "{}")
        self._name = f"{name}.json"
        self._code = code

    def get_code(self) -> str:
        return json.dumps(self._code, indent=2)
