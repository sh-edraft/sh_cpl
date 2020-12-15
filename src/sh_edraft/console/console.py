import os
from typing import Union, Optional
from termcolor import colored

from sh_edraft.console.model.background_color import BackgroundColor
from sh_edraft.console.model.foreground_color import ForegroundColor


class Console:
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
        if cls._disabled:
            return

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

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def close():
        Console.reset()
        Console.write('\n\n\nPress any key to continue...')
        Console.read_line()
        exit()

    @classmethod
    def disable(cls):
        cls._disabled = True

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
        if output is not None:
            cls.write(output)

        return input()

    @classmethod
    def reset(cls):
        cls._background_color = BackgroundColor.default
        cls._foreground_color = ForegroundColor.default

    @classmethod
    def write(cls, *args):
        string = ' '.join(map(str, args))
        cls._output(string, end='')

    @classmethod
    def write_at(cls, x: int, y: int, *args):
        string = ' '.join(map(str, args))
        cls._output(string, x, y, end='')

    @classmethod
    def write_line(cls, *args):
        string = ' '.join(map(str, args))
        cls._output('')
        cls._output(string, end='')

    @classmethod
    def write_line_at(cls, x: int, y: int, *args):
        string = ' '.join(map(str, args))
        cls._output('', end='')
        cls._output(string, x, y, end='')
