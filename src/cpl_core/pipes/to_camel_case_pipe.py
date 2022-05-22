import string

from cpl_core.pipes import PipeABC


class ToCamelCasePipe(PipeABC):

    def __init__(self): pass

    def transform(self, value: str, *args) -> str:
        r"""Converts string to camel case

        Parameter
        ---------
            chars: :class:`str`
                String to convert

        Returns
        -------
            String converted to CamelCase
        """
        converted_name = value
        char_set = string.punctuation + ' '
        for char in char_set:
            if char in converted_name:
                converted_name = ''.join(word.title() for word in converted_name.split(char))

        return converted_name
