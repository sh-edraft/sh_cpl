import re

from cpl_core.pipes import PipeABC


class ToSnakeCasePipe(PipeABC):

    def __init__(self): pass

    def transform(self, value: str, *args) -> str:
        r"""Converts string to snake case

        Parameter
        ---------
            chars: :class:`str`
                String to convert

        Returns
        -------
            String converted to snake_case
        """
        # convert to train-case to CamelCase
        if '-' in value:
            value = ''.join(word.title() for word in value.split('-'))

        pattern1 = re.compile(r'(.)([A-Z][a-z]+)')
        pattern2 = re.compile(r'([a-z0-9])([A-Z])')
        file_name = re.sub(pattern1, r'\1_\2', value)
        return re.sub(pattern2, r'\1_\2', file_name).lower()
