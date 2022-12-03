from abc import ABC, abstractmethod
from itertools import islice

from cpl_query.base.sequence_values import SequenceValues


class SequenceABC(ABC):

    @abstractmethod
    def __init__(self, t: type = None, values: list = None):
        ABC.__init__(self)
        if values is None:
            values = []

        if t is None and len(values) > 0:
            t = type(values[0])

        if t is None:
            t = any

        self._type = t
        self._set_values(values)

    @classmethod
    def __class_getitem__(cls, _t: type):
        return _t

    def __len__(self):
        return len(self._values)

    def __iter__(self):
        return iter(self._values)

    def next(self):
        return next(self._values)

    def __next__(self):
        return self.next()

    def __getitem__(self, n):
        values = [x for x in self]
        if isinstance(n, slice):
            try:
                return values[n]
            except Exception as e:
                raise e

        for i in range(len(values)):
            if i == n:
                return values[i]

    def __repr__(self):
        return f'<{type(self).__name__} {list(self).__repr__()}>'

    @property
    def type(self) -> type:
        return self._type

    def _check_type(self, __object: any):
        if self._type == any:
            return

        if self._type is not None and type(__object) != self._type and not isinstance(type(__object), self._type) and not issubclass(type(__object), self._type):
            raise Exception(f'Unexpected type: {type(__object)}\nExpected type: {self._type}')

    def _set_values(self, values: list):
        self._values = SequenceValues(values, self._type)

    def to_list(self) -> list:
        r"""Converts :class: `cpl_query.base.sequence_abc.SequenceABC` to :class: `list`

        Returns
        -------
            :class: `list`
        """
        return [x for x in self]

    def copy(self) -> 'SequenceABC':
        r"""Creates a copy of sequence

        Returns
        -------
            SequenceABC
        """
        return type(self)(self._type, self.to_list())

    @classmethod
    def empty(cls) -> 'SequenceABC':
        r"""Returns an empty sequence

        Returns
        -------
            Sequence object that contains no elements
        """
        return cls()

    def index(self, _object: object) -> int:
        r"""Returns the index of given element

        Returns
        -------
            Index of object

        Raises
        -------
            IndexError if object not in sequence
        """
        for i, o in enumerate(self):
            if o == _object:
                return i

        raise IndexError

    @classmethod
    def range(cls, start: int, length: int) -> 'SequenceABC':
        return cls(int, list(range(start, length)))
