import textwrap

from cpl.utils.string import String
from cpl_cli._templates.template_file_abc import TemplateFileABC


class MainWithApplicationHostAndStartupTemplate(TemplateFileABC):

    def __init__(self, name: str, path: str):
        TemplateFileABC.__init__(self)

        name = String.convert_to_snake_case(name)
        self._name = 'main.py'
        self._path = path

        import_pkg = f'{name}.'

        self._value = textwrap.dedent(f"""\
            from cpl.application import ApplicationBuilder
            
            from {import_pkg}application import Application
            from {import_pkg}startup import Startup
            
            
            def main():
                app_builder = ApplicationBuilder(Application)
                app_builder.use_startup(Startup)
                app_builder.build().run()
            
            
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


class MainWithApplicationBaseTemplate(TemplateFileABC):

    def __init__(self, name: str, path: str):
        TemplateFileABC.__init__(self)

        name = String.convert_to_snake_case(name)
        self._name = 'main.py'
        self._path = path

        import_pkg = f'{name}.'

        self._value = textwrap.dedent(f"""\
            from cpl.application import ApplicationBuilder
            
            from {import_pkg}application import Application
            
            
            def main():
                app_builder = ApplicationBuilder(Application)
                app_builder.build().run()
            
            
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


class MainWithoutApplicationBaseTemplate(TemplateFileABC):

    def __init__(self, name: str, path: str):
        TemplateFileABC.__init__(self)

        name = String.convert_to_snake_case(name)
        self._name = 'main.py'
        self._path = path

        import_pkg = f'{name}.'

        self._value = textwrap.dedent("""\
            from cpl.console import Console
            
            
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


class MainWithDependencyInjection(TemplateFileABC):

    def __init__(self, name: str, path: str):
        TemplateFileABC.__init__(self)

        name = String.convert_to_snake_case(name)
        self._name = 'main.py'
        self._path = path

        import_pkg = f'{name}.'

        self._value = textwrap.dedent("""\
            from cpl.configuration import Configuration, ConfigurationABC
            from cpl.console import Console
            from cpl.dependency_injection import ServiceCollection, ServiceProviderABC
            
            
            def configure_configuration() -> ConfigurationABC:
                config = Configuration()
                return config
            
            
            def configure_services(config: ConfigurationABC) -> ServiceProviderABC:
                services = ServiceCollection(config)
                return services.build_service_provider()
            
            
            def main():
                config = configure_configuration()
                provider = configure_services(config)
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
