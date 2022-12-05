import textwrap

from cpl_cli.abc.generate_schematic_abc import GenerateSchematicABC


class Pipe(GenerateSchematicABC):

    def __init__(self, *args: str):
        GenerateSchematicABC.__init__(self, *args)

    def get_code(self) -> str:
        code = """\
        from cpl_core.pipes.pipe_abc import PipeABC
        
        
        class $Name(PipeABC):

            def __init__(self): pass
        
            def transform(self, value: any, *args):
                return value
        """
        x = self.build_code_str(code, Name=self._class_name)
        return x

    @classmethod
    def register(cls):
        GenerateSchematicABC.register(
            cls,
            'pipe',
            ['p', 'P']
        )
