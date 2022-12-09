from cpl_cli.abc.generate_schematic_abc import GenerateSchematicABC


class Enum(GenerateSchematicABC):

    def __init__(self, *args: str):
        GenerateSchematicABC.__init__(self, *args)

    def get_code(self) -> str:
        import textwrap
        code = textwrap.dedent("""\
        from enum import Enum
        
        
        class $Name(Enum):
        
            atr = 0
        """)
        return self.build_code_str(code, Name=self._class_name)

    @classmethod
    def register(cls):
        GenerateSchematicABC.register(
            cls,
            'enum',
            ['e', 'E']
        )
