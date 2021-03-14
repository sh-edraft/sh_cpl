from cpl.console import ForegroundColorEnum
from cpl.console.console import Console


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

