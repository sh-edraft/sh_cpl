from enum import Enum


# models
class ExceptionArgument(Enum):
    list = "list"
    func = "func"
    type = "type"
    value = "value"
    index = "index"


# exceptions
class ArgumentNoneException(Exception):
    r"""Exception when argument is None"""

    def __init__(self, arg: ExceptionArgument):
        Exception.__init__(self, f"argument {arg} is None")


class IndexOutOfRangeException(Exception):
    r"""Exception when index is out of range"""

    def __init__(self, err: str = None):
        Exception.__init__(self, f"List index out of range" if err is None else err)


class InvalidTypeException(Exception):
    r"""Exception when type is invalid"""
    pass


class WrongTypeException(Exception):
    r"""Exception when type is unexpected"""
    pass
