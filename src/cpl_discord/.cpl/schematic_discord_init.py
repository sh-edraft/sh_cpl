import textwrap

from cpl_cli.abc.generate_schematic_abc import GenerateSchematicABC


class DiscordBotInit(GenerateSchematicABC):
    def __init__(self, *args: str):
        GenerateSchematicABC.__init__(self, *args)
        self._name = f"__init__.py"

    def get_code(self) -> str:
        code = """\
        # imports
        """
        return self.build_code_str(code, Name=self._class_name)

    @classmethod
    def register(cls):
        GenerateSchematicABC.register(cls, "init", [])
