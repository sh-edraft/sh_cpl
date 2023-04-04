from cpl_cli.abc.code_file_template_abc import CodeFileTemplateABC
from cpl_core.utils import String


class DiscordBotProjectFileMain(CodeFileTemplateABC):
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
            import asyncio
            from typing import Optional
            
            from cpl_core.application import ApplicationBuilder, ApplicationABC
            from {import_pkg}application import Application
            from {import_pkg}startup import Startup
            
            
            class Program:
            
                def __init__(self):
                    self._app: Optional[Application] = None
            
                async def main(self):
                    app_builder = ApplicationBuilder(Application)
                    app_builder.use_startup(Startup)
                    self._app: ApplicationABC = await app_builder.build_async()
                    await self._app.run_async()
            
                async def stop(self):
                    await self._app.stop_async()
            
            
            if __name__ == '__main__':
                program = Program()
                try:
                    asyncio.run(program.main())
                except KeyboardInterrupt:
                    asyncio.run(program.stop())
        """
        )

    def get_code(self) -> str:
        return self._main_with_application_host_and_startup
