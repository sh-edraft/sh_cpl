import re
import string
import random


class String:
    r"""Useful functions for strings"""

    @staticmethod
    def convert_to_camel_case(chars: str) -> str:
        r"""Converts string to camel case

        Parameter
        ---------
            chars: :class:`str`
                String to convert

        Returns
        -------
            String converted to CamelCase
        """
        converted_name = chars
        char_set = string.punctuation + ' '
        for char in char_set:
            if char in converted_name:
                converted_name = ''.join(word.title() for word in converted_name.split(char))

        return converted_name

    @staticmethod
    def convert_to_snake_case(chars: str) -> str:
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
        if '-' in chars:
            chars = ''.join(word.title() for word in chars.split('-'))

        pattern1 = re.compile(r'(.)([A-Z][a-z]+)')
        pattern2 = re.compile(r'([a-z0-9])([A-Z])')
        file_name = re.sub(pattern1, r'\1_\2', chars)
        return re.sub(pattern2, r'\1_\2', file_name).lower()

    @staticmethod
    def first_to_upper(chars: str) -> str:
        r"""Converts first char to upper

        Parameter
        ---------
            chars: :class:`str`
                String to convert

        Returns
        -------
            String with first char as upper
        """
        return f'{chars[0].upper()}{chars[1:]}'

    @staticmethod
    def first_to_lower(chars: str) -> str:
        r"""Converts first char to lower

        Parameter
        ---------
            chars: :class:`str`
                String to convert

        Returns
        -------
            String with first char as lower
        """
        return f'{chars[0].lower()}{chars[1:]}'

    @staticmethod
    def random_string(chars: str, length: int) -> str:
        r"""Creates random string by given chars and length

        Returns
        -------
            String of random chars
        """

        return ''.join(random.choice(chars) for _ in range(length))
