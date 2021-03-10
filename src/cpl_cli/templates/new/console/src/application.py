import textwrap

from cpl_cli.templates.template_file_abc import TemplateFileABC


class ApplicationTemplate(TemplateFileABC):

    def __init__(self):
        TemplateFileABC.__init__(self)

        self._name = 'application.py'
        self._path = 'src/'
        self._value = textwrap.dedent("""\
            from cpl.application.application_abc import ApplicationABC
            from cpl.console.console import Console
            
            
            class Application(ApplicationABC):
            
                def __init__(self):
                    ApplicationABC.__init__(self)
            
                def configure(self):
                    pass
            
                def main(self):
                    Console.write_line('Hello World')
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
