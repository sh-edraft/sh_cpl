import textwrap

from cpl_cli.templates.template_file_abc import TemplateFileABC


class CLIInitTemplate(TemplateFileABC):

    def __init__(self, name: str):
        TemplateFileABC.__init__(self)

        self._name = '__init__.py'
        self._path = f'src/{name}_cli/'
        self._value = textwrap.dedent("""\
            # imports: 
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
