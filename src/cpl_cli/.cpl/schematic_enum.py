import textwrap

from cpl_cli.abc.generate_schematic_abc import GenerateSchematicABC


class Enum(GenerateSchematicABC):

    def __init__(self, *args: str):
        GenerateSchematicABC.__init__(self, *args)

    def get_code(self) -> str:
        code = """\
        from enum import Enum
        
        
        class $Name(Enum):
        
            atr = 0
        """
        x = self.build_code_str(code, Name=self._class_name)
        return x

    @classmethod
    def register(cls):
        GenerateSchematicABC.register(
            cls,
            'enum',
            ['e', 'E']
        )
