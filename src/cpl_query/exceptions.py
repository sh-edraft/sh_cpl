from enum import Enum


# models
class ExceptionArgument(Enum):
    list = 'list'
    func = 'func'
    type = 'type'
    value = 'value'
    index = 'index'


# exceptions
class ArgumentNoneException(Exception):

    def __init__(self, arg: ExceptionArgument):
        Exception.__init__(self, f'Argument {arg} is None')


class InvalidTypeException(Exception):
    pass


class WrongTypeException(Exception):
    pass
