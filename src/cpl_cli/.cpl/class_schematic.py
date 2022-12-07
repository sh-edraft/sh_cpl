from cpl_cli.abc.generate_schematic_abc import GenerateSchematicABC
from cpl_core.utils import String


class Class(GenerateSchematicABC):

    def __init__(self, name: str, path: str, schematic: str):
        GenerateSchematicABC.__init__(self, name, path, schematic)
        self._name = f'{String.convert_to_snake_case(name)}.py'
        self._class_name = f'{String.first_to_upper(name)}'

    def get_code(self) -> str:
        code = """\
        class $Name:

            def __init__(self):
                pass
        """
        x = self.build_code_str(code, Name=self._class_name)
        return x

    @classmethod
    def register(cls):
        GenerateSchematicABC.register(
            cls,
            'class',
            ['c', 'C']
        )
