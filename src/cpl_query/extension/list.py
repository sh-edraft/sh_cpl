from cpl_query.extension.iterable import Iterable


class List(Iterable):

    def __init__(self, t: type = None, values: list = None):
        Iterable.__init__(self)

        self._type = t

        if values is not None:
            self.extend(values)
