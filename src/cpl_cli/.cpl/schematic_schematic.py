from cpl_cli.abc.generate_schematic_abc import GenerateSchematicABC
from cpl_core.utils import String


class Schematic(GenerateSchematicABC):

    def __init__(self, name: str, path: str, schematic: str):
        GenerateSchematicABC.__init__(self, name, path, schematic)
        self._name = f'schematic_{String.convert_to_snake_case(name)}.py'
        self._path = '.cpl/'
        self._class_name = String.convert_to_camel_case(name)

    def get_code(self) -> str:
        code = """\
        from cpl_cli.abc.generate_schematic_abc import GenerateSchematicABC


        class $Name(GenerateSchematicABC):
        
            def __init__(self, *args: str):
                GenerateSchematicABC.__init__(self, *args)
        
            def get_code(self) -> str:
                import textwrap
                code = textwrap.dedent(\"\"\"\\
                from enum import Enum
                
                
                class $Name(Enum):
                
                    atr = 0
                \"\"\")
                return self.build_code_str(code, Name=self._class_name)
        
            @classmethod
            def register(cls):
                GenerateSchematicABC.register(
                    cls,
                    '$NameLower',
                    []
                )
        """
        return self.build_code_str(code, Name=self._class_name, NameLower=self._class_name.lower())

    @classmethod
    def register(cls):
        GenerateSchematicABC.register(
            cls,
            'schematic',
            ['scheme', 'SCHEME']
        )
