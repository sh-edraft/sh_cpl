from enum import Enum


class ConfigurationVariableNameEnum(Enum):
    environment = "ENVIRONMENT"
    name = "NAME"
    customer = "CUSTOMER"

    @staticmethod
    def to_list():
        return [var.value for var in ConfigurationVariableNameEnum]
