import textwrap

from cpl_cli.templates.template_file_abc import TemplateFileABC


class MainWithApplicationHostAndStartupTemplate(TemplateFileABC):

    def __init__(self):
        TemplateFileABC.__init__(self)

        self._name = 'main.py'
        self._path = 'src/'
        self._value = textwrap.dedent("""\
            from startup import Startup
            from application import Application
            
            
            def main():
                app = Application()
                app.use_startup(Startup)
                app.build()
                app.run()
            
            
            if __name__ == '__main__':
                main()
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


class MainWithApplicationHostTemplate(TemplateFileABC):

    def __init__(self):
        TemplateFileABC.__init__(self)

        self._name = 'main.py'
        self._path = 'src/'
        self._value = textwrap.dedent("""\
            from application import Application
            
            
            def main():
                app = Application()
                app.build()
                app.run()
            
            
            if __name__ == '__main__':
                main()
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


class MainWithoutApplicationHostTemplate(TemplateFileABC):

    def __init__(self):
        TemplateFileABC.__init__(self)

        self._name = 'main.py'
        self._path = 'src/'
        self._value = textwrap.dedent("""\
            from cpl.console.console import Console
            
            
            def main():
                Console.write_line('Hello World')
            
            
            if __name__ == '__main__':
                main()
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
