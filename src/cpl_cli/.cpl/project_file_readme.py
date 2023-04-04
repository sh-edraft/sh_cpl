from cpl_cli.abc.file_template_abc import FileTemplateABC


class ProjectFileReadme(FileTemplateABC):
    def __init__(self, path: str):
        FileTemplateABC.__init__(self, "", path, "")
        self._name = "README.md"

    def get_code(self) -> str:
        return self._code
