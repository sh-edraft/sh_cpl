from cpl_cli.abc.code_file_template_abc import CodeFileTemplateABC
from cpl_core.utils import String


class ProjectFileMain(CodeFileTemplateABC):
    def __init__(
        self,
        name: str,
        path: str,
        use_application_api: bool,
        use_startup: bool,
        use_service_providing: bool,
        use_async: bool,
    ):
        CodeFileTemplateABC.__init__(
            self, "main", path, "", use_application_api, use_startup, use_service_providing, use_async
        )

        import textwrap

        import_pkg = f"{String.convert_to_snake_case(name)}."

        self._main_with_application_host_and_startup = textwrap.dedent(
            f"""\
            {"import asyncio" if self._use_async else ''}
            
            from cpl_core.application import ApplicationBuilder
                
            from {import_pkg}application import Application
            from {import_pkg}startup import Startup
                
                
            {self._async()}def main():
                app_builder = ApplicationBuilder(Application)
                app_builder.use_startup(Startup)
                {"app: Application = await app_builder.build_async()" if self._use_async else ""}
                {"await app.run_async()" if self._use_async else "app_builder.build().run()"}
                
                
            if __name__ == '__main__':
                {"asyncio.run(main())" if self._use_async else "main()"}
        """
        )
        self._main_with_application_base = textwrap.dedent(
            f"""\
            {"import asyncio" if self._use_async else ''}
            
            from cpl_core.application import ApplicationBuilder
                
            from {import_pkg}application import Application
                
                
            {self._async()}def main():
                app_builder = ApplicationBuilder(Application)
                {"app: Application = await app_builder.build_async()" if self._use_async else ""}
                {"await app.run_async()" if self._use_async else "app_builder.build().run()"}
                
                
            if __name__ == '__main__':
                {"asyncio.run(main())" if self._use_async else "main()"}
        """
        )

        self._main_with_dependency_injection = textwrap.dedent(
            f"""\
            {"import asyncio" if self._use_async else ''}
            
            from cpl_core.application import ApplicationBuilder
            
            
            {self._async()}def configure_configuration() -> ConfigurationABC:
                    config = Configuration()
                    return config
                
                
            {self._async()}def configure_services(config: ConfigurationABC) -> ServiceProviderABC:
                services = ServiceCollection(config)
                return services.build_service_provider()
            
                
            {self._async()}def main():
                config = {self._async()}configure_configuration()
                provider = {self._async()}configure_services(config)
                Console.write_line('Hello World')
                
                
            if __name__ == '__main__':
                {"asyncio.run(main())" if self._use_async else "main()"}
        """
        )

    def _async(self) -> str:
        if self._use_async:
            return "async "
        return ""

    def get_code(self) -> str:
        if self._use_application_api and self._use_startup:
            return self._main_with_application_host_and_startup

        if self._use_application_api:
            return self._main_with_application_base

        if self._use_service_providing:
            return self._main_with_dependency_injection

        return self._main_with_application_base
