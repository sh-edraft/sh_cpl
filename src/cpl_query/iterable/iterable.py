from typing import Iterable as IterableType

from cpl_query.iterable.iterable_abc import IterableABC


def _default_lambda(x: object):
    return x


class Iterable(IterableABC):

    def __init__(self, t: type = None, values: IterableType = None):
        IterableABC.__init__(self, t, values)
