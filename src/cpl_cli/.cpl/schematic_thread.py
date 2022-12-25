import textwrap

from cpl_cli.abc.generate_schematic_abc import GenerateSchematicABC


class Thread(GenerateSchematicABC):

    def __init__(self, *args: str):
        GenerateSchematicABC.__init__(self, *args)

    def get_code(self) -> str:
        code = """\
        import threading
        
        
        class $Name(threading.Thread):

            def __init__(self):
                threading.Thread.__init__(self)
                
            def run(self) -> None:
                pass
        """
        x = self.build_code_str(code, Name=self._class_name)
        return x

    @classmethod
    def register(cls):
        GenerateSchematicABC.register(
            cls,
            'thread',
            ['t', 'T']
        )
