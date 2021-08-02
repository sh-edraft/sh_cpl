from .._extension.iterable import Iterable


class List(Iterable):

    def __init__(self, t: type = None, values: list = None):
        Iterable.__init__(self, t, values)
