import textwrap
from string import Template


class ABCTemplate:

    @staticmethod
    def get_abc_py(name: str) -> str:
        string = textwrap.dedent("""\
        from abc import ABC, abstractmethod


        class $Name(ABC):
        
            @abstractmethod
            def __init__(self): pass

        """)

        return Template(string).substitute(
            Name=name
        )
