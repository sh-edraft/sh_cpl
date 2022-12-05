import textwrap

from cpl_cli.abc.generate_schematic_abc import GenerateSchematicABC


class ABC(GenerateSchematicABC):

    def __init__(self, *args):
        GenerateSchematicABC.__init__(self, *args)

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
