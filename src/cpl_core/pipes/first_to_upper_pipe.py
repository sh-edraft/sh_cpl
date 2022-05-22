from cpl_core.pipes.pipe_abc import PipeABC


class FirstToUpperPipe(PipeABC):

    def __init__(self): pass

    def transform(self, value: str, *args):
        r"""Converts first char to upper

        Parameter
        ---------
            chars: :class:`str`
                String to convert

        Returns
        -------
            String with first char as upper
        """
        return f'{value[0].upper()}{value[1:]}'
