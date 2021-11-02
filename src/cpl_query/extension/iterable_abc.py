from abc import ABC, abstractmethod
from typing import Optional, Callable, Union, Iterable


class IterableABC(ABC, list):
    r"""ABC to define functions on list
    """

    @abstractmethod
    def __init__(self, t: type = None, values: list = None):
        list.__init__(self)

        if t == any:
            t = None
        self._type = t

        if values is not None:
            for value in values:
                self.append(value)

    @property
    def type(self) -> type:
        return self._type

    @abstractmethod
    def all(self, func: Callable) -> bool:
        r"""Checks if every element of list equals result found by function

        Parameter
        ---------
            func: :class:`Callable`
                selected value

        Returns
        -------
            bool
        """
        pass

    @abstractmethod
    def any(self, func: Callable) -> bool:
        r"""Checks if list contains result found by function

        Parameter
        ---------
            func: :class:`Callable`
                selected value

        Returns
        -------
            bool
        """
        pass

    def append(self, __object: object) -> None:
        r"""Adds element to list

        Parameter
        ---------
            __object: :class:`object`
                value
        """
        if self._type is not None and type(__object) != self._type and not isinstance(type(__object), self._type) \
                and not issubclass(type(__object), self._type):
            raise Exception(f'Unexpected type: {type(__object)}')

        if len(self) == 0 and self._type is None:
            self._type = type(__object)

        super().append(__object)

    @abstractmethod
    def average(self, func: Callable = None) -> Union[int, float, complex]:
        r"""Returns average value of list

        Parameter
        ---------
            func: :class:`Callable`
                selected value

        Returns
        -------
            Union[int, float, complex]
        """
        pass

    @abstractmethod
    def contains(self, value: object) -> bool:
        r"""Checks if list contains value given by function

        Parameter
        ---------
            value: :class:`object`
                value

        Returns
        -------
            bool
        """
        pass

    @abstractmethod
    def count(self, func: Callable) -> int:
        r"""Returns length of list or count of found elements

        Parameter
        ---------
            func: :class:`Callable`
                selected value

        Returns
        -------
            int
        """
        pass

    @abstractmethod
    def distinct(self, func: Callable) -> 'IterableABC':
        r"""Returns list without redundancies

        Parameter
        ---------
            func: :class:`Callable`
                selected value

        Returns
        -------
            :class: `cpl_query.extension.iterable_abc.IterableABC`
        """
        pass

    @abstractmethod
    def element_at(self, index: int) -> any:
        r"""Returns element at given index

        Parameter
        ---------
            index: :class:`int`
                index

        Returns
        -------
            Value at index: any
        """
        pass

    @abstractmethod
    def element_at_or_default(self, index: int) -> Optional[any]:
        r"""Returns element at given index or None

        Parameter
        ---------
            index: :class:`int`
                index

        Returns
        -------
            Value at index: Optional[any]
        """
        pass

    def extend(self, __iterable: Iterable) -> None:
        r"""Adds elements of given list to list

        Parameter
        ---------
            __iterable: :class: `cpl_query.extension.iterable.Iterable`
                index
        """
        for value in __iterable:
            self.append(value)

    @abstractmethod
    def last(self) -> any:
        r"""Returns last element

        Returns
        -------
            Last element of list: any
        """
        pass

    @abstractmethod
    def last_or_default(self) -> any:
        r"""Returns last element or None

        Returns
        -------
            Last element of list: Optional[any]
        """
        pass

    @abstractmethod
    def first(self) -> any:
        r"""Returns first element

        Returns
        -------
            First element of list: any
        """
        pass

    @abstractmethod
    def first_or_default(self) -> any:
        r"""Returns first element or None

        Returns
        -------
            First element of list: Optional[any]
        """
        pass

    @abstractmethod
    def for_each(self, func: Callable):
        r"""Runs given function for each element of list

        Parameter
        ---------
            func: :class: `Callable`
                function to call
        """
        pass

    @abstractmethod
    def max(self, func: Callable = None) -> Union[int, float, complex]:
        r"""Returns highest value

        Parameter
        ---------
            func: :class:`Callable`
                selected value

        Returns
        -------
            Union[int, float, complex]
        """
        pass

    @abstractmethod
    def min(self, func: Callable = None) -> Union[int, float, complex]:
        r"""Returns highest value

        Parameter
        ---------
            func: :class:`Callable`
                selected value

        Returns
        -------
            Union[int, float, complex]
        """
        pass

    @abstractmethod
    def order_by(self, func: Callable) -> 'IterableABC':
        r"""Sorts elements by function in ascending order

        Parameter
        ---------
            func: :class:`Callable`
                selected value

        Returns
        -------
            :class: `cpl_query.extension.iterable_abc.IterableABC`
        """
        pass

    @abstractmethod
    def order_by_descending(self, func: Callable) -> 'IterableABC':
        r"""Sorts elements by function in descending order

        Parameter
        ---------
            func: :class:`Callable`
                selected value

        Returns
        -------
            :class: `cpl_query.extension.iterable_abc.IterableABC`
        """
        pass

    @abstractmethod
    def reverse(self) -> 'IterableABC':
        r"""Reverses list

        Returns
        -------
            :class: `cpl_query.extension.iterable_abc.IterableABC`
        """
        pass

    @abstractmethod
    def single(self) -> any:
        r"""Returns one single element of list

        Returns
        -------
            Found value: any

        Raises
        ------
            ArgumentNoneException: when argument is None
            Exception: when argument is None or found more than one element
        """
        pass

    @abstractmethod
    def single_or_default(self) -> Optional[any]:
        r"""Returns one single element of list

        Returns
        -------
            Found value: Optional[any]
        """
        pass

    @abstractmethod
    def skip(self, index: int) -> 'IterableABC':
        r"""Skips all elements from index

        Parameter
        ---------
            index: :class:`int`
                index

        Returns
        -------
            :class: `cpl_query.extension.iterable_abc.IterableABC`
        """
        pass

    @abstractmethod
    def skip_last(self, index: int) -> 'IterableABC':
        r"""Skips all elements after index

        Parameter
        ---------
            index: :class:`int`
                index

        Returns
        -------
            :class: `cpl_query.extension.iterable_abc.IterableABC`
        """
        pass

    @abstractmethod
    def sum(self, func: Callable = None) -> Union[int, float, complex]:
        r"""Sum of all values

        Parameter
        ---------
            func: :class:`Callable`
                selected value

        Returns
        -------
            Union[int, float, complex]
        """
        pass

    @abstractmethod
    def take(self, index: int) -> 'IterableABC':
        r"""Takes all elements from index

        Parameter
        ---------
            index: :class:`int`
                index

        Returns
        -------
            :class: `cpl_query.extension.iterable_abc.IterableABC`
        """
        pass

    @abstractmethod
    def take_last(self, index: int) -> 'IterableABC':
        r"""Takes all elements after index

        Parameter
        ---------
            index: :class:`int`
                index

        Returns
        -------
            :class: `cpl_query.extension.iterable_abc.IterableABC`
        """
        pass

    def to_list(self) -> list:
        r"""Converts :class: `cpl_query.extension.iterable_abc.IterableABC` to :class: `list`

        Returns
        -------
            :class: `list`
        """
        return list(self)

    @abstractmethod
    def where(self, func: Callable) -> 'IterableABC':
        r"""Select element by function

        Parameter
        ---------
            func: :class:`Callable`
                selected value

        Returns
        -------
            :class: `cpl_query.extension.iterable_abc.IterableABC`
        """
        pass
