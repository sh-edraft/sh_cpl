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
        Exception.__init__(self, f'argument {arg} is None')


class IndexOutOfRangeException(Exception):

    def __init__(self):
        Exception.__init__(self, f'List index out of range')


class InvalidTypeException(Exception):
    pass


class WrongTypeException(Exception):
    pass
