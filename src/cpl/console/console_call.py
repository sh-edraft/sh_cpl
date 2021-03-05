from collections import Callable


class ConsoleCall:

    def __init__(self, function: Callable, *args):
        self._func = function
        self._args = args

    @property
    def function(self):
        return self._func

    @property
    def args(self):
        return self._args
