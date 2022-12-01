from cpl_query.enumerable.enumerable_abc import EnumerableABC


def _default_lambda(x: object):
    return x


class Enumerable(EnumerableABC):
    r"""Implementation of :class: `cpl_query.enumerable.enumerable_abc.EnumerableABC`
    """

    def __init__(self, t: type = None, values: list = None):
        EnumerableABC.__init__(self, t, values)
