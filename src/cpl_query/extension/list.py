from iterable import Iterable


class List(Iterable):
    r"""Implementation of :class: `cpl_query.Iterable`
    """

    def __init__(self, t: type = None, values: list = None):
        Iterable.__init__(self, t, values)
