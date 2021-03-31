from cpl_cli.templates.template_file_abc import TemplateFileABC


class ReadmeTemplate(TemplateFileABC):

    def __init__(self):
        TemplateFileABC.__init__(self)

        self._name = 'README.md'
        self._path = ''
        self._value = """"""

    @property
    def name(self) -> str:
        return self._name

    @property
    def path(self) -> str:
        return self._path

    @property
    def value(self) -> str:
        return self._value
