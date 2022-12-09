from cpl_cli.abc.generate_schematic_abc import GenerateSchematicABC
from cpl_core.utils import String


class ABC(GenerateSchematicABC):

    def __init__(self, name: str, schematic: str, path: str):
        GenerateSchematicABC.__init__(self, name, schematic, path)
        self._class_name = name
        if name != '':
            self._class_name = f'{String.first_to_upper(name.replace(schematic, ""))}ABC'

    def get_code(self) -> str:
        code = """\
        from abc import ABC, abstractmethod


        class $Name(ABC):
        
            @abstractmethod
            def __init__(self): pass
        """
        x = self.build_code_str(code, Name=self._class_name)
        return x

    @classmethod
    def register(cls):
        GenerateSchematicABC.register(
            cls,
            'abc',
            ['a', 'A']
        )
