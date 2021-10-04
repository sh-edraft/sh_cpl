from cpl_core.console.foreground_color_enum import ForegroundColorEnum
from cpl_core.console.console import Console


class Error:

    @staticmethod
    def error(message: str):
        Console.error(message)
        Console.error('Run \'cpl help\'\n')

    @staticmethod
    def warn(message: str):
        Console.set_foreground_color(ForegroundColorEnum.yellow)
        Console.write_line(message)
        Console.set_foreground_color(ForegroundColorEnum.default)

