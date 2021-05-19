import textwrap

from cpl_cli._templates.template_file_abc import TemplateFileABC


class TestsInitTemplate(TemplateFileABC):

    def __init__(self):
        TemplateFileABC.__init__(self)

        self._name = '__init__.py'
        self._path = 'src/tests/'
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