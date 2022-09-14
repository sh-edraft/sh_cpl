import io
import itertools

from cpl_query.exceptions import IndexOutOfRangeException


class SequenceEnd:

    def __init__(self):
        self.is_ended = False

    def set_end(self, value: bool) -> 'SequenceEnd':
        self.is_ended = value
        return self


class SequenceValues:
    def __init__(self, data, _t: type):
        if data is None:
            data = []

        if len(data) > 0:
            def type_check(_t: type, _l: list):
                return all(isinstance(x, _t) for x in _l)

            if not type_check(_t, data):
                raise Exception(f'Unexpected type\nExpected type: {_t}')

        if not hasattr(data, '__iter__'):
            raise TypeError(f'{type(self).__name__} must be instantiated with an iterable object')

        self._data = data
        self._index = 0
        self._cycle = itertools.cycle(self._data)

    def __len__(self):
        return sum(1 for item in self._data)

    def __iter__(self):
        i = 0
        while i < len(self):
            yield next(self._cycle)
            i += 1

    def __next__(self):
        if self._index >= len(self):
            raise IndexOutOfRangeException()
        self._index += 1

        return self.next()

    def next(self):
        return next(self._cycle)

    def reset(self):
        self._index = 0
        self._cycle = itertools.cycle(self._data)
