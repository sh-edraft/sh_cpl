from cpl_core.utils import String


class SchematicCollection:
    _schematics: dict = {}

    @classmethod
    def register(cls, template: type, schematic: str, aliases: list[str]):
        cls._schematics[schematic] = {
            "Template": template,
            "Aliases": aliases
        }

    @classmethod
    def get_schematics(cls) -> dict:
        return cls._schematics
