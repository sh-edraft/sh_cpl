import os
import subprocess
from typing import Union
from termcolor import colored

from sh_edraft.utils.console.model.background_color import BackgroundColor
from sh_edraft.utils.console.model.foreground_color import ForegroundColor


class Console:
    _background_color: BackgroundColor = BackgroundColor.default
    _foreground_color: ForegroundColor = ForegroundColor.default

    @property
    def background_color(self) -> BackgroundColor:
        return self._background_color

    @property
    def foreground_color(self) -> ForegroundColor:
        return self._foreground_color

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

    # useful methods
    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def new():
        if os.name == 'nt':
            os.system("start /wait cmd")
        else:
            p = subprocess.Popen(args=["gnome-terminal"])
            p.communicate()

    @staticmethod
    def read(output: str = None) -> str:
        user_input = input(output if output else '')
        return user_input[0]

    @staticmethod
    def read_line(output: str = None) -> str:
        return input(output if output else '')

    @classmethod
    def reset(cls):
        cls._background_color = BackgroundColor.default
        cls._foreground_color = ForegroundColor.default

    @classmethod
    def write(cls, string: str):
        if cls._foreground_color == ForegroundColor.default:
            print(colored(string), end='')
        else:
            print(colored(string, cls._foreground_color.value), end='')

    @classmethod
    def write_line(cls, *args):
        string = ' '.join(map(str, args))
        if cls._foreground_color == ForegroundColor.default:
            print(colored(string))
        else:
            print(colored(string, cls._foreground_color.value))
