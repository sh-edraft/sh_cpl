from abc import ABC, abstractmethod


class Sequence(list):

    @abstractmethod
    def __init__(self, t: type = None, values: list = None):
        list.__init__(self)
        ABC.__init__(self)
        values = [] if values is None else values
        list.__init__(self, values)

        if t is None and len(values) > 0:
            t = type(values[0])

        if t is None:
            t = any

        self._type = t

    @classmethod
    def __class_getitem__(cls, _t: type):
        return _t

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

    def to_list(self) -> list:
        r"""Converts :class: `cpl_query.base.sequence_abc.SequenceABC` to :class: `list`

        Returns
        -------
            :class: `list`
        """
        return [x for x in self]

    def copy(self) -> 'Sequence':
        r"""Creates a copy of sequence

        Returns
        -------
            Sequence
        """
        return type(self)(self._type, self.to_list())

    @classmethod
    def empty(cls) -> 'Sequence':
        r"""Returns an empty sequence

        Returns
        -------
            Sequence object that contains no elements
        """
        return cls()

    def index_of(self, _object: object) -> int:
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
    def range(cls, start: int, length: int) -> 'Sequence':
        return cls(int, list(range(start, length)))
