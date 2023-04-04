from typing import Iterable as TIterable

from cpl_query.iterable.iterable_abc import IterableABC


def _default_lambda(x: object):
    return x


class Iterable(IterableABC):
    def __init__(self, t: type = None, values: TIterable = None):
        IterableABC.__init__(self, t, values)
