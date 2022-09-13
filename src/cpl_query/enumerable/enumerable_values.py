import io
import itertools


class EnumerableValues:
    def __init__(self, data):
        if data is None:
            data = []

        if not hasattr(data, '__iter__'):
            raise TypeError('RepeatableIterable must be instantiated with an iterable object')

        is_generator = hasattr(data, 'gi_running') or isinstance(data, io.TextIOBase)
        self._data = data if not is_generator else [i for i in data]
        self._len = sum(1 for item in self._data)
        self.cycle = itertools.cycle(self._data)

    def __len__(self):
        return self._len

    def __iter__(self):
        i = 0
        while i < len(self):
            yield next(self.cycle)
            i += 1

    def __next__(self):
        return self.next()

    def next(self):
        return next(self.cycle)
