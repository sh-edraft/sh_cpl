import os
from typing import Union, Optional

import pyfiglet
from tabulate import tabulate
from termcolor import colored

from cpl.console.background_color import BackgroundColor
from cpl.console.foreground_color import ForegroundColor


class Console:
    _is_first_write = True

    _background_color: BackgroundColor = BackgroundColor.default
    _foreground_color: ForegroundColor = ForegroundColor.default
    _x: Optional[int] = None
    _y: Optional[int] = None
    _disabled: bool = False

    """
        Properties
    """

    @classmethod
    @property
    def background_color(cls) -> str:
        return str(cls._background_color.value)

    @classmethod
    @property
    def foreground_color(cls) -> str:
        return str(cls._foreground_color.value)

    """
        Settings
    """

    @classmethod
    def set_background_color(cls, color: Union[BackgroundColor, str]):
        if type(color) is str:
            cls._background_color = BackgroundColor[color]
        else:
            cls._background_color = color

    @classmethod
    def set_foreground_color(cls, color: Union[ForegroundColor, str]):

        if type(color) is str:
            cls._foreground_color = ForegroundColor[color]
        else:
            cls._foreground_color = color

    @classmethod
    def reset_cursor_position(cls):
        cls._x = None
        cls._y = None

    @classmethod
    def set_cursor_position(cls, x: int, y: int):
        cls._x = x
        cls._y = y

    """
        Useful protected methods
    """

    @classmethod
    def _output(cls, string: str, x: int = None, y: int = None, end='\n'):
        if cls._is_first_write:
            cls._is_first_write = False

        args = []
        colored_args = []

        if x is not None and y is not None:
            args.append(f'\033[{x};{y}H')
        elif cls._x is not None and cls._y is not None:
            args.append(f'\033[{cls._x};{cls._y}H')

        colored_args.append(string)
        if cls._foreground_color != ForegroundColor.default and cls._background_color == BackgroundColor.default:
            colored_args.append(cls._foreground_color.value)
        elif cls._foreground_color == ForegroundColor.default and cls._background_color != BackgroundColor.default:
            colored_args.append(cls._background_color.value)
        elif cls._foreground_color != ForegroundColor.default and cls._background_color != BackgroundColor.default:
            colored_args.append(cls._foreground_color.value)
            colored_args.append(cls._background_color.value)

        args.append(colored(*colored_args))
        print(*args, end=end)

    """
        Useful public methods
    """

    @classmethod
    def banner(cls, string: str):
        if cls._disabled:
            return

        ascii_banner = pyfiglet.figlet_format(string)
        cls.write_line(ascii_banner)

    @classmethod
    def clear(cls):
        os.system('cls' if os.name == 'nt' else 'clear')

    @classmethod
    def close(cls):
        if cls._disabled:
            return

        Console.reset()
        Console.write('\n\n\nPress any key to continue...')
        Console.read_line()
        exit()

    @classmethod
    def disable(cls):
        cls._disabled = True

    @classmethod
    def error(cls, string: str, tb: str = None):
        if cls._disabled:
            return

        cls.set_foreground_color('red')
        if tb is not None:
            cls.write_line(f'{string} -> {tb}')
        else:
            cls.write_line(string)
        cls.set_foreground_color('default')

    @classmethod
    def enable(cls):
        cls._disabled = False

    @classmethod
    def read(cls, output: str = None) -> str:
        if output is not None:
            cls.write(output)

        return input()[0]

    @classmethod
    def read_line(cls, output: str = None) -> str:
        if cls._disabled:
            return ''

        if output is not None:
            cls.write(output)

        return input()

    @classmethod
    def reset(cls):
        cls._background_color = BackgroundColor.default
        cls._foreground_color = ForegroundColor.default

    @classmethod
    def table(cls, header: list[str], values: list[list[str]]):
        if cls._disabled:
            return

        table = tabulate(values, headers=header)

        Console.write_line(table)
        Console.write('\n')

    @classmethod
    def write(cls, *args):
        if cls._disabled:
            return

        string = ' '.join(map(str, args))
        cls._output(string, end='')

    @classmethod
    def write_at(cls, x: int, y: int, *args):
        if cls._disabled:
            return

        string = ' '.join(map(str, args))
        cls._output(string, x, y, end='')

    @classmethod
    def write_line(cls, *args):
        if cls._disabled:
            return

        string = ' '.join(map(str, args))
        if not cls._is_first_write:
            cls._output('')
        cls._output(string, end='')

    @classmethod
    def write_line_at(cls, x: int, y: int, *args):
        if cls._disabled:
            return

        string = ' '.join(map(str, args))
        if not cls._is_first_write:
            cls._output('', end='')
        cls._output(string, x, y, end='')
