import textwrap
from abc import abstractmethod
from string import Template

from cpl_cli.abc.file_template_abc import FileTemplateABC
from cpl_cli.configuration.schematic_collection import SchematicCollection
from cpl_core.utils import String


class GenerateSchematicABC(FileTemplateABC):
    def __init__(self, name: str, schematic: str, path: str):
        FileTemplateABC.__init__(self, name, path, "")
        self._name = f"{String.convert_to_snake_case(name)}_{schematic}.py"
        if schematic in name.lower():
            self._name = f"{String.convert_to_snake_case(name)}.py"

        self._class_name = name
        if name != "":
            self._class_name = f"{String.first_to_upper(name)}{String.first_to_upper(schematic)}"

        if schematic in name.lower():
            self._class_name = f"{String.first_to_upper(name)}"

    @property
    def class_name(self) -> str:
        return self._class_name

    @abstractmethod
    def get_code(self) -> str:
        pass

    @classmethod
    def build_code_str(cls, code: str, **kwargs) -> str:
        text = textwrap.dedent(code)
        return Template(text).substitute(**kwargs)

    @classmethod
    @abstractmethod
    def register(cls, *args):
        SchematicCollection.register(*args)
