from .._extension.iterable import Iterable


class List(Iterable):

    def __init__(self, t: type = None, values: list = None):
        Iterable.__init__(self)

        self._type = t

        if values is not None:
            self.extend(values)

    def append(self, __object: object) -> None:
        if self._type is not None and type(__object) != self._type and not isinstance(type(__object), self._type):
            raise Exception(f'Unexpected type: {type(__object)}')

        super().append(__object)
