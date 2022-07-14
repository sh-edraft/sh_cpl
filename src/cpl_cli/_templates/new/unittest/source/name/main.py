import textwrap

from cpl_core.utils.string import String
from cpl_cli._templates.template_file_abc import TemplateFileABC


class MainWithApplicationBaseTemplate(TemplateFileABC):

    def __init__(self, name: str, path: str, use_async: bool):
        TemplateFileABC.__init__(self)

        name = String.convert_to_snake_case(name)
        self._name = 'main.py'
        self._path = path

        import_pkg = f'{name}.'

        if use_async:
            self._value = textwrap.dedent(f"""\
                import asyncio
                
                from cpl_core.application import ApplicationBuilder
                
                from {import_pkg}application import Application
                
                
                async def main():
                    app_builder = ApplicationBuilder(Application)
                    app: Application = await app_builder.build_async()
                    await app.run_async()
                
                
                if __name__ == '__main__':
                    asyncio.run(main())
            """)
        else:
            self._value = textwrap.dedent(f"""\
                from cpl_core.application import ApplicationBuilder
                
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
