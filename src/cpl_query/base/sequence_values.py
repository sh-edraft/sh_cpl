import io
import itertools

from cpl_query.exceptions import IndexOutOfRangeException


class SequenceValues:
    def __init__(self, data: list, _t: type):
        if len(data) > 0:
            def type_check(_t: type, _l: list):
                return all([_t == any or isinstance(x, _t) for x in _l])

            if not type_check(_t, data):
                print([type(x) for x in data])
                raise Exception(f'Unexpected type\nExpected type: {_t}')

        if not hasattr(data, '__iter__'):
            raise TypeError(f'{type(self).__name__} must be instantiated with an iterable object')

        self._new_cycle = lambda: itertools.cycle(data)
        self._len = lambda: len(data)

        self._index = 0
        self._cycle = self._new_cycle()

    def __len__(self):
        return self._len()

    def __iter__(self):
        i = 0
        while i < self._len():
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
        self._cycle = self._new_cycle()
