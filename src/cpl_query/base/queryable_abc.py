from abc import abstractmethod, ABC
from typing import Optional, Callable, Union


class QueryableABC(ABC):

    @abstractmethod
    def all(self, _func: Callable) -> bool:
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
    def any(self, _func: Callable) -> bool:
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

    @abstractmethod
    def average(self, _func: Callable) -> Union[int, float, complex]:
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
    def count(self, _func: Callable = None) -> int:
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
    def distinct(self, _func: Callable = None) -> 'QueryableABC':
        r"""Returns list without redundancies

        Parameter
        ---------
            func: :class:`Callable`
                selected value

        Returns
        -------
            :class: `cpl_query.base.queryable_abc.QueryableABC`
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
    def for_each(self, _func: Callable):
        r"""Runs given function for each element of list

        Parameter
        ---------
            func: :class: `Callable`
                function to call
        """
        pass

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
    def max(self, _func: Callable) -> Union[int, float, complex]:
        r"""Returns the highest value

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
    def median(self) -> Union[int, float]:
        r"""Return the median value of data elements

        Returns
        -------
            Union[int, float]
        """
        pass


    @abstractmethod
    def min(self, _func: Callable) -> Union[int, float, complex]:
        r"""Returns the lowest value

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
    def order_by(self, _func: Callable) -> 'QueryableABC':
        r"""Sorts elements by function in ascending order

        Parameter
        ---------
            func: :class:`Callable`
                selected value

        Returns
        -------
            :class: `cpl_query.base.queryable_abc.QueryableABC`
        """
        pass

    @abstractmethod
    def order_by_descending(self, _func: Callable) -> 'QueryableABC':
        r"""Sorts elements by function in descending order

        Parameter
        ---------
            func: :class:`Callable`
                selected value

        Returns
        -------
            :class: `cpl_query.base.queryable_abc.QueryableABC`
        """
        pass

    @abstractmethod
    def reverse(self) -> 'QueryableABC':
        r"""Reverses list

        Returns
        -------
            :class: `cpl_query.base.queryable_abc.QueryableABC`
        """
        pass

    @abstractmethod
    def select(self, _f: Callable) -> 'QueryableABC':
        r"""Formats each element of list to a given format

        Returns
        -------
            :class: `cpl_query.base.queryable_abc.QueryableABC`
        """
        pass

    @abstractmethod
    def select_many(self, _f: Callable) -> 'QueryableABC':
        r"""Flattens resulting lists to one

        Returns
        -------
            :class: `cpl_query.base.queryable_abc.QueryableABC`
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
    def skip(self, index: int) -> 'QueryableABC':
        r"""Skips all elements from index

        Parameter
        ---------
            index: :class:`int`
                index

        Returns
        -------
            :class: `cpl_query.base.queryable_abc.QueryableABC`
        """
        pass

    @abstractmethod
    def skip_last(self, index: int) -> 'QueryableABC':
        r"""Skips all elements after index

        Parameter
        ---------
            index: :class:`int`
                index

        Returns
        -------
            :class: `cpl_query.base.queryable_abc.QueryableABC`
        """
        pass

    @abstractmethod
    def sum(self, _func: Callable) -> Union[int, float, complex]:
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
    def take(self, index: int) -> 'QueryableABC':
        r"""Takes all elements from index

        Parameter
        ---------
            index: :class:`int`
                index

        Returns
        -------
            :class: `cpl_query.base.queryable_abc.QueryableABC`
        """
        pass

    @abstractmethod
    def take_last(self, index: int) -> 'QueryableABC':
        r"""Takes all elements after index

        Parameter
        ---------
            index: :class:`int`
                index

        Returns
        -------
            :class: `cpl_query.base.queryable_abc.QueryableABC`
        """
        pass

    @abstractmethod
    def where(self, _func: Callable) -> 'QueryableABC':
        r"""Select element by function

        Parameter
        ---------
            func: :class:`Callable`
                selected value

        Returns
        -------
            :class: `cpl_query.base.queryable_abc.QueryableABC`
        """
        pass
