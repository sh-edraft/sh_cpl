import os
from collections import Callable
from typing import Union, Optional

import pyfiglet
from pynput import keyboard
from pynput.keyboard import Key
from tabulate import tabulate
from termcolor import colored

from cpl.console.background_color_enum import BackgroundColorEnum
from cpl.console.console_call import ConsoleCall
from cpl.console.foreground_color_enum import ForegroundColorEnum
from cpl.console.spinner_thread import SpinnerThread


class Console:
    _is_first_write = True

    _background_color: BackgroundColorEnum = BackgroundColorEnum.default
    _foreground_color: ForegroundColorEnum = ForegroundColorEnum.default
    _x: Optional[int] = None
    _y: Optional[int] = None
    _disabled: bool = False

    _hold_back = False
    _hold_back_calls: list[ConsoleCall] = []

    _select_menu_items: list[str] = []
    _is_first_select_menu_output = True
    _selected_menu_item_index: int = 0
    _selected_menu_item_char: str = ''
    _selected_menu_option_foreground_color: ForegroundColorEnum = ForegroundColorEnum.default
    _selected_menu_option_background_color: BackgroundColorEnum = BackgroundColorEnum.default
    _selected_menu_cursor_foreground_color: ForegroundColorEnum = ForegroundColorEnum.default
    _selected_menu_cursor_background_color: BackgroundColorEnum = BackgroundColorEnum.default

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
    def set_hold_back(cls, value: bool):
        cls._hold_back = value

    @classmethod
    def set_background_color(cls, color: Union[BackgroundColorEnum, str]):
        if type(color) is str:
            cls._background_color = BackgroundColorEnum[color]
        else:
            cls._background_color = color

    @classmethod
    def set_foreground_color(cls, color: Union[ForegroundColorEnum, str]):

        if type(color) is str:
            cls._foreground_color = ForegroundColorEnum[color]
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
            args.append(f'\033[{y};{x}H')
        elif cls._x is not None and cls._y is not None:
            args.append(f'\033[{cls._y};{cls._x}H')

        colored_args.append(string)
        if cls._foreground_color != ForegroundColorEnum.default and cls._background_color == BackgroundColorEnum.default:
            colored_args.append(cls._foreground_color.value)
        elif cls._foreground_color == ForegroundColorEnum.default and cls._background_color != BackgroundColorEnum.default:
            colored_args.append(cls._background_color.value)
        elif cls._foreground_color != ForegroundColorEnum.default and cls._background_color != BackgroundColorEnum.default:
            colored_args.append(cls._foreground_color.value)
            colored_args.append(cls._background_color.value)

        args.append(colored(*colored_args))
        print(*args, end=end)

    @classmethod
    def _show_select_menu(cls):
        if not cls._is_first_select_menu_output:
            for _ in range(0, len(cls._select_menu_items) + 1):
                print('\b', end="\r")
        else:
            cls._is_first_select_menu_output = False

        for i in range(0, len(cls._select_menu_items)):
            Console.set_foreground_color(cls._selected_menu_cursor_foreground_color)
            Console.set_background_color(cls._selected_menu_cursor_background_color)
            Console.write_line(f'{cls._selected_menu_item_char if cls._selected_menu_item_index == i else " "} ')
            Console.set_foreground_color(cls._selected_menu_option_foreground_color)
            Console.set_background_color(cls._selected_menu_option_background_color)
            Console.write(f'{cls._select_menu_items[i]}')

        Console.write_line()

    @classmethod
    def _select_menu_key_press(cls, key: Key):
        if key == Key.down:
            if cls._selected_menu_item_index == len(cls._select_menu_items) - 1:
                return
            cls._selected_menu_item_index += 1
            cls._show_select_menu()

        elif key == Key.up:
            if cls._selected_menu_item_index == 0:
                return
            cls._selected_menu_item_index -= 1
            cls._show_select_menu()

        elif key == Key.enter:
            return False

    """
        Useful public methods
    """

    @classmethod
    def banner(cls, string: str):
        if cls._disabled:
            return

        if cls._hold_back:
            cls._hold_back_calls.append(ConsoleCall(cls.banner, string))
            return

        ascii_banner = pyfiglet.figlet_format(string)
        cls.write_line(ascii_banner)

    @classmethod
    def clear(cls):
        if cls._hold_back:
            cls._hold_back_calls.append(ConsoleCall(cls.clear))
            return

        os.system('cls' if os.name == 'nt' else 'clear')

    @classmethod
    def close(cls):
        if cls._disabled:
            return

        if cls._hold_back:
            cls._hold_back_calls.append(ConsoleCall(cls.close))
            return

        Console.color_reset()
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

        if cls._hold_back:
            cls._hold_back_calls.append(ConsoleCall(cls.error, string, tb))
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
        if output is not None and not cls._hold_back:
            cls.write_line(output)

        return input()[0]

    @classmethod
    def read_line(cls, output: str = None) -> str:
        if cls._disabled and not cls._hold_back:
            return ''

        if output is not None:
            cls.write_line(output)

        cls._output('\n', end='')

        return input()

    @classmethod
    def color_reset(cls):
        cls._background_color = BackgroundColorEnum.default
        cls._foreground_color = ForegroundColorEnum.default

    @classmethod
    def table(cls, header: list[str], values: list[list[str]]):
        if cls._disabled:
            return

        if cls._hold_back:
            cls._hold_back_calls.append(ConsoleCall(cls.table, header, values))
            return

        table = tabulate(values, headers=header)

        Console.write_line(table)
        Console.write('\n')

    @classmethod
    def select(cls, char: str, message: str, options: list[str],
               header_foreground_color: Union[str, ForegroundColorEnum] = ForegroundColorEnum.default,
               header_background_color: Union[str, BackgroundColorEnum] = BackgroundColorEnum.default,
               option_foreground_color: Union[str, ForegroundColorEnum] = ForegroundColorEnum.default,
               option_background_color: Union[str, BackgroundColorEnum] = BackgroundColorEnum.default,
               cursor_foreground_color: Union[str, ForegroundColorEnum] = ForegroundColorEnum.default,
               cursor_background_color: Union[str, BackgroundColorEnum] = BackgroundColorEnum.default
               ) -> str:

        cls._selected_menu_item_char = char
        cls._select_menu_items = options

        if option_foreground_color is not None:
            cls._selected_menu_option_foreground_color = option_foreground_color
        if option_background_color is not None:
            cls._selected_menu_option_background_color = option_background_color

        if cursor_foreground_color is not None:
            cls._selected_menu_cursor_foreground_color = cursor_foreground_color
        if cursor_background_color is not None:
            cls._selected_menu_cursor_background_color = cursor_background_color

        Console.set_foreground_color(header_foreground_color)
        Console.set_background_color(header_background_color)
        Console.write_line(message)
        cls._show_select_menu()

        with keyboard.Listener(
                on_press=cls._select_menu_key_press, suppress=True) as listener:
            listener.join()

        Console.color_reset()
        return cls._select_menu_items[cls._selected_menu_item_index]

    @classmethod
    def spinner(cls, message: str, call: Callable, *args, text_foreground_color: Union[str, ForegroundColorEnum] = None,
                spinner_foreground_color: Union[str, ForegroundColorEnum] = None,
                text_background_color: Union[str, BackgroundColorEnum] = None,
                spinner_background_color: Union[str, BackgroundColorEnum] = None) -> any:
        if cls._hold_back:
            cls._hold_back_calls.append(ConsoleCall(cls.spinner, message, call, *args))
            return

        if text_foreground_color is not None:
            cls.set_foreground_color(text_foreground_color)

        if text_background_color is not None:
            cls.set_background_color(text_background_color)

        cls.write_line(message)
        cls.set_hold_back(True)
        spinner = SpinnerThread(len(message), spinner_foreground_color, spinner_background_color)
        spinner.start()
        return_value = call(*args)
        spinner.stop_spinning()
        cls.set_hold_back(False)

        cls.set_foreground_color(ForegroundColorEnum.default)
        cls.set_background_color(BackgroundColorEnum.default)

        for call in cls._hold_back_calls:
            call.function(*call.args)

        return return_value

    @classmethod
    def write(cls, *args):
        if cls._disabled:
            return

        if cls._hold_back:
            cls._hold_back_calls.append(ConsoleCall(cls.write, args))
            return

        string = ' '.join(map(str, args))
        cls._output(string, end='')

    @classmethod
    def write_at(cls, x: int, y: int, *args):
        if cls._disabled:
            return

        if cls._hold_back:
            cls._hold_back_calls.append(ConsoleCall(cls.write_at, x, y, args))
            return

        string = ' '.join(map(str, args))
        cls._output(string, x, y, end='')

    @classmethod
    def write_line(cls, *args):
        if cls._disabled:
            return

        if cls._hold_back:
            cls._hold_back_calls.append(ConsoleCall(cls.write_line, args))
            return

        string = ' '.join(map(str, args))
        if not cls._is_first_write:
            cls._output('')
        cls._output(string, end='')

    @classmethod
    def write_line_at(cls, x: int, y: int, *args):
        if cls._disabled:
            return

        if cls._hold_back:
            cls._hold_back_calls.append(ConsoleCall(cls.write_line_at, x, y, args))
            return

        string = ' '.join(map(str, args))
        if not cls._is_first_write:
            cls._output('', end='')
        cls._output(string, x, y, end='')
