from cpl_core.pipes.pipe_abc import PipeABC


class FirstCharToLowerPipe(PipeABC):

    def __init__(self): pass

    def transform(self, value: any, *args):
        r"""Converts first char to lower

        Parameter
        ---------
            value: :class:`str`
                String to convert

        Returns
        -------
            String with first char as lower
        """
        return f'{value[0].lower()}{value[1:]}'
