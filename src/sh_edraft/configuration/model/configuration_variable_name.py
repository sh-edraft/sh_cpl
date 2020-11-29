from enum import Enum


class ConfigurationVariableName(Enum):

    environment = 'ENVIRONMENT'
    name = 'NAME'
    customer = 'CUSTOMER'

    @staticmethod
    def to_list():
        return [var.value for var in ConfigurationVariableName]
