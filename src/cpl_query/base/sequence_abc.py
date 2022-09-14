from abc import abstractmethod, ABC
from typing import Union

from cpl_query.base.sequence_values import SequenceValues


class SequenceABC(ABC):

    @abstractmethod
    def __init__(self, t: type = None, values: Union[list, iter] = None):
        ABC.__init__(self)

        if t == any:
            t = None
        elif t is None and values is not None:
            t = type(values[0])

        self._type = t
        self._values = SequenceValues(values, t)

    def __len__(self):
        return len(self._values)

    def __iter__(self):
        return iter(self._values)

    def next(self):
        return next(self._values)

    def __next__(self):
        return self.next()

    def __repr__(self):
        return f'<{type(self).__name__} {list(self).__repr__()}>'

    @property
    def type(self) -> type:
        return self._type

    def reset(self):
        self._values.reset()

    def to_list(self) -> list:
        r"""Converts :class: `cpl_query.base.sequence_abc.SequenceABC` to :class: `list`

        Returns
        -------
            :class: `list`
        """
        return [x for x in self]
