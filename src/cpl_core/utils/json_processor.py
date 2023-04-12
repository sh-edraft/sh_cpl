import enum
from inspect import signature, Parameter

from cpl_core.utils import String


class JSONProcessor:
    @staticmethod
    def process(_t: type, values: dict) -> object:
        args = []

        sig = signature(_t.__init__)
        for param in sig.parameters.items():
            parameter = param[1]
            if parameter.name == "self" or parameter.annotation == Parameter.empty:
                continue

            name = String.first_to_upper(String.convert_to_camel_case(parameter.name))
            name_first_lower = String.first_to_lower(name)
            if name in values or name_first_lower in values or name.upper() in values:
                value = ""
                if name in values:
                    value = values[name]
                elif name_first_lower in values:
                    value = values[name_first_lower]
                else:
                    value = values[name.upper()]

                if isinstance(value, dict) and not issubclass(parameter.annotation, dict):
                    value = JSONProcessor.process(parameter.annotation, value)

                if issubclass(parameter.annotation, enum.Enum):
                    value = parameter.annotation[value]

                if type(value) != parameter.annotation:
                    value = parameter.annotation(value)

                args.append(value)

            elif parameter.default != Parameter.empty:
                args.append(parameter.default)

            else:
                args.append(None)

        return _t(*args)
