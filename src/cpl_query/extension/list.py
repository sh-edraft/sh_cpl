from cpl_query.extension.iterable import Iterable


class List(Iterable):
    r"""Implementation of :class: `cpl_query.extension.iterable.Iterable`
    """

    def __init__(self, t: type = None, values: list = None):
        Iterable.__init__(self, t, values)
