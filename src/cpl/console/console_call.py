from collections import Callable


class ConsoleCall:
    r"""Represents a console call, for hold back when spinner is active

    Parameter
    ---------
        function: :class:`Callable`
            Function to call
        args: :class:`list`
            List of arguments
    """

    def __init__(self, function: Callable, *args):
        self._func = function
        self._args = args

    @property
    def function(self):
        return self._func

    @property
    def args(self):
        return self._args
