import textwrap

from cpl_cli.abc.generate_schematic_abc import GenerateSchematicABC


class Init(GenerateSchematicABC):

    def __init__(self, *args: str):
        GenerateSchematicABC.__init__(self, *args)
        self._name = f'__init__.py'

    def get_code(self) -> str:
        code = """\
        # imports
        """
        x = self.build_code_str(code, Name=self._class_name)
        return x

    @classmethod
    def register(cls):
        GenerateSchematicABC.register(
            cls,
            'init',
            []
        )
