import os
import sys
import time
from collections.abc import Callable
from typing import Union, Optional

from art import text2art
import colorama
from tabulate import tabulate
from termcolor import colored

from cpl_core.console.background_color_enum import BackgroundColorEnum
from cpl_core.console.console_call import ConsoleCall
from cpl_core.console.foreground_color_enum import ForegroundColorEnum
from cpl_core.console.spinner_thread import SpinnerThread


class Console:
    r"""Useful functions for handling with input and output"""
    colorama.init()
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

    """Properties"""

    @classmethod
    @property
    def background_color(cls) -> str:
        return str(cls._background_color.value)

    @classmethod
    @property
    def foreground_color(cls) -> str:
        return str(cls._foreground_color.value)

    """Settings"""

    @classmethod
    def set_hold_back(cls, value: bool):
        cls._hold_back = value

    @classmethod
    def set_background_color(cls, color: Union[BackgroundColorEnum, str]):
        r"""Sets the background color

        Parameter
        ---------
            color: Union[:class:`cpl_core.console.background_color_enum.BackgroundColorEnum`, :class:`str`]
                Background color of the console
        """
        if type(color) is str:
            cls._background_color = BackgroundColorEnum[color]
        else:
            cls._background_color = color

    @classmethod
    def set_foreground_color(cls, color: Union[ForegroundColorEnum, str]):
        r"""Sets the foreground color

        Parameter
        ---------
            color: Union[:class:`cpl_core.console.background_color_enum.BackgroundColorEnum`, :class:`str`]
                Foreground color of the console
        """
        if type(color) is str:
            cls._foreground_color = ForegroundColorEnum[color]
        else:
            cls._foreground_color = color

    @classmethod
    def reset_cursor_position(cls):
        r"""Resets cursor position"""
        cls._x = None
        cls._y = None

    @classmethod
    def set_cursor_position(cls, x: int, y: int):
        r"""Sets cursor position

        Parameter
        ---------
            x: :class:`int`
                X coordinate
            y: :class:`int`
                Y coordinate
        """
        cls._x = x
        cls._y = y

    """Useful protected functions"""

    @classmethod
    def _output(cls, string: str, x: int = None, y: int = None, end: str = None):
        r"""Prints given output with given format

        Parameter
        ---------
            string: :class:`str`
                Message to print
            x: :class:`int`
                X coordinate
            y: :class:`int`
                Y coordinate
            end: :class:`str`
                End character of the message (could be \n)
        """
        if cls._is_first_write:
            cls._is_first_write = False

        if end is None:
            end = '\n'

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
        r"""Shows the select menu"""
        if not cls._is_first_select_menu_output:
            for _ in range(0, len(cls._select_menu_items) + 1):
                sys.stdout.write('\x1b[1A\x1b[2K')
        else:
            cls._is_first_select_menu_output = False

        for i in range(0, len(cls._select_menu_items)):
            Console.set_foreground_color(cls._selected_menu_cursor_foreground_color)
            Console.set_background_color(cls._selected_menu_cursor_background_color)
            placeholder = ''
            for _ in cls._selected_menu_item_char:
                placeholder += ' '

            Console.write_line(
                f'{cls._selected_menu_item_char if cls._selected_menu_item_index == i else placeholder} ')
            Console.set_foreground_color(cls._selected_menu_option_foreground_color)
            Console.set_background_color(cls._selected_menu_option_background_color)
            Console.write(f'{cls._select_menu_items[i]}')

        Console.write_line()

    @classmethod
    def _select_menu_key_press(cls, key):
        r"""Event function when key press is detected

        Parameter
        ---------
            key: :class:`pynput.keyboard.Key`
                Pressed key
        """
        from pynput.keyboard import Key
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

    """ Useful public functions"""

    @classmethod
    def banner(cls, string: str):
        r"""Prints the string as a banner

        Parameter
        ---------
            string: :class:`str`
                Message to print as banner
        """
        if cls._disabled:
            return

        if cls._hold_back:
            cls._hold_back_calls.append(ConsoleCall(cls.banner, string))
            return

        cls.write_line(text2art(string))

    @classmethod
    def color_reset(cls):
        r"""Resets the color settings"""
        cls._background_color = BackgroundColorEnum.default
        cls._foreground_color = ForegroundColorEnum.default

    @classmethod
    def clear(cls):
        r"""Clears the console"""
        if cls._hold_back:
            cls._hold_back_calls.append(ConsoleCall(cls.clear))
            return

        os.system('cls' if os.name == 'nt' else 'clear')

    @classmethod
    def close(cls):
        r"""Closes the application"""
        if cls._disabled:
            return

        if cls._hold_back:
            cls._hold_back_calls.append(ConsoleCall(cls.close))
            return

        Console.color_reset()
        Console.write('\n\n\nPress any key to continue...')
        Console.read()
        sys.exit()

    @classmethod
    def disable(cls):
        r"""Disables console interaction"""
        cls._disabled = True

    @classmethod
    def error(cls, string: str, tb: str = None):
        r"""Prints an error with traceback

        Parameter
        ---------
            string: :class:`str`
                Error message
            tb: :class:`str`
                Error traceback
        """
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
        r"""Enables console interaction"""
        cls._disabled = False

    @classmethod
    def read(cls, output: str = None) -> str:
        r"""Reads in line

        Parameter
        ---------
            output: :class:`str`
                String to print before input

        Returns
        -------
            input()
        """
        if output is not None and not cls._hold_back:
            cls.write_line(output)

        return input()

    @classmethod
    def read_line(cls, output: str = None) -> str:
        r"""Reads in next line

        Parameter
        ---------
            output: :class:`str`
                String to print before input

        Returns
        -------
            input()
        """
        if cls._disabled and not cls._hold_back:
            return ''

        if output is not None:
            cls.write_line(output)

        cls._output('\n', end='')

        return input()

    @classmethod
    def table(cls, header: list[str], values: list[list[str]]):
        r"""Prints a table with header and values

        Parameter
        ---------
            header: List[:class:`str`]
                Header of the table
            values: List[List[:class:`str`]]
                Values of the table
        """
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
        r"""Prints select menu

        Parameter
        ---------
            char: :class:`str`
                Character to show which element is selected
            message: :class:`str`
                Message or header of the selection
            options: List[:class:`str`]
                Selectable options
            header_foreground_color: Union[:class:`str`, :class:`cpl_core.console.foreground_color_enum.ForegroundColorEnum`]
                Foreground color of the header
            header_background_color: Union[:class:`str`, :class:`cpl_core.console.background_color_enum.BackgroundColorEnum`]
                Background color of the header
            option_foreground_color: Union[:class:`str`, :class:`cpl_core.console.foreground_color_enum.ForegroundColorEnum`]
                Foreground color of the options
            option_background_color: Union[:class:`str`, :class:`cpl_core.console.background_color_enum.BackgroundColorEnum`]
                Background color of the options
            cursor_foreground_color: Union[:class:`str`, :class:`cpl_core.console.foreground_color_enum.ForegroundColorEnum`]
                Foreground color of the cursor
            cursor_background_color: Union[:class:`str`, :class:`cpl_core.console.background_color_enum.BackgroundColorEnum`]
                Background color of the cursor

        Returns
        -------
            Selected option as :class:`str`
        """
        cls._selected_menu_item_char = char
        cls.options = options
        cls._select_menu_items = cls.options

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
        Console.write_line(message, '\n')
        cls._show_select_menu()

        from pynput import keyboard
        with keyboard.Listener(
                on_press=cls._select_menu_key_press, suppress=False
        ) as listener:
            listener.join()

        Console.color_reset()
        return cls._select_menu_items[cls._selected_menu_item_index]

    @classmethod
    def spinner(cls, message: str, call: Callable, *args, text_foreground_color: Union[str, ForegroundColorEnum] = None,
                spinner_foreground_color: Union[str, ForegroundColorEnum] = None,
                text_background_color: Union[str, BackgroundColorEnum] = None,
                spinner_background_color: Union[str, BackgroundColorEnum] = None, **kwargs) -> any:
        r"""Shows spinner and calls given function, when function has ended the spinner stops

        Parameter
        ---------
            message: :class:`str`
                Message of the spinner
            call: :class:`Callable`
                Function to call
            args: :class:`list`
                Arguments of the function
            text_foreground_color: Union[:class:`str`, :class:`cpl_core.console.foreground_color_enum.ForegroundColorEnum`]
                Foreground color of the text
            spinner_foreground_color: Union[:class:`str`, :class:`cpl_core.console.foreground_color_enum.ForegroundColorEnum`]
                Foreground color of the spinner
            text_background_color: Union[:class:`str`, :class:`cpl_core.console.background_color_enum.BackgroundColorEnum`]
                Background color of the text
            spinner_background_color: Union[:class:`str`, :class:`cpl_core.console.background_color_enum.BackgroundColorEnum`]
                Background color of the spinner
            kwargs: :class:`dict`
                Keyword arguments of the call

        Returns
        -------
            Return value of call
        """
        if cls._hold_back:
            cls._hold_back_calls.append(ConsoleCall(cls.spinner, message, call, *args))
            return

        if text_foreground_color is not None:
            cls.set_foreground_color(text_foreground_color)

        if text_background_color is not None:
            cls.set_background_color(text_background_color)

        if type(spinner_foreground_color) is str:
            spinner_foreground_color = ForegroundColorEnum[spinner_foreground_color]

        if type(spinner_background_color) is str:
            spinner_background_color = BackgroundColorEnum[spinner_background_color]

        cls.write_line(message)
        cls.set_hold_back(True)
        spinner = None
        if not cls._disabled:
            spinner = SpinnerThread(len(message), spinner_foreground_color, spinner_background_color)
            spinner.start()

        return_value = None
        try:
            return_value = call(*args, **kwargs)
        except KeyboardInterrupt:
            if spinner is not None:
                spinner.exit()
            cls.close()

        if spinner is not None:
            spinner.stop_spinning()
        cls.set_hold_back(False)

        cls.set_foreground_color(ForegroundColorEnum.default)
        cls.set_background_color(BackgroundColorEnum.default)

        for call in cls._hold_back_calls:
            call.function(*call.args)

        cls._hold_back_calls = []

        time.sleep(0.1)

        return return_value

    @classmethod
    def write(cls, *args, end=''):
        r"""Prints in active line

        Parameter
        ---------
            args: :class:`list`
                Elements to print
            end: :class:`str`
                Last character to print
        """
        if cls._disabled:
            return

        if cls._hold_back:
            cls._hold_back_calls.append(ConsoleCall(cls.write, *args))
            return

        string = ' '.join(map(str, args))
        cls._output(string, end=end)

    @classmethod
    def write_at(cls, x: int, y: int, *args):
        r"""Prints at given position

        Parameter
        ---------
            x: :class:`int`
                X coordinate
            y: :class:`int`
                Y coordinate
            args: :class:`list`
                Elements to print
        """
        if cls._disabled:
            return

        if cls._hold_back:
            cls._hold_back_calls.append(ConsoleCall(cls.write_at, x, y, *args))
            return

        string = ' '.join(map(str, args))
        cls._output(string, x, y, end='')

    @classmethod
    def write_line(cls, *args):
        r"""Prints to new line

        Parameter
        ---------
            args: :class:`list`
                Elements to print
        """
        if cls._disabled:
            return

        if cls._hold_back:
            cls._hold_back_calls.append(ConsoleCall(cls.write_line, *args))
            return

        string = ' '.join(map(str, args))
        if not cls._is_first_write:
            cls._output('')
        cls._output(string, end='')

    @classmethod
    def write_line_at(cls, x: int, y: int, *args):
        r"""Prints new line at given position

        Parameter
        ---------
            x: :class:`int`
                X coordinate
            y: :class:`int`
                Y coordinate
            args: :class:`list`
                Elements to print
        """
        if cls._disabled:
            return

        if cls._hold_back:
            cls._hold_back_calls.append(ConsoleCall(cls.write_line_at, x, y, *args))
            return

        string = ' '.join(map(str, args))
        if not cls._is_first_write:
            cls._output('', end='')
        cls._output(string, x, y, end='')
