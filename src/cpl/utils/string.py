import re


class String:

    @staticmethod
    def convert_to_snake_case(name: str) -> str:
        pattern1 = re.compile(r'(.)([A-Z][a-z]+)')
        pattern2 = re.compile(r'([a-z0-9])([A-Z])')
        file_name = re.sub(pattern1, r'\1_\2', name)
        return re.sub(pattern2, r'\1_\2', file_name).lower()

    @staticmethod
    def first_to_upper(string: str) -> str:
        return f'{string[0].upper()}{string[1:]}'

    @staticmethod
    def first_to_lower(string: str) -> str:
        return f'{string[0].lower()}{string[1:]}'
