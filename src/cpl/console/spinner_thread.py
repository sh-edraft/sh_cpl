import os
import sys
import threading
import time

from termcolor import colored

from cpl.console.background_color_enum import BackgroundColorEnum
from cpl.console.foreground_color_enum import ForegroundColorEnum


class SpinnerThread(threading.Thread):

    def __init__(self, msg_len: int, foreground_color: ForegroundColorEnum, background_color: BackgroundColorEnum):
        """
        Thread to show spinner in terminal
        :param msg_len:
        :param foreground_color:
        :param background_color:
        """
        threading.Thread.__init__(self)

        self._msg_len = msg_len
        self._foreground_color = foreground_color
        self._background_color = background_color

        self._is_spinning = True
        self._exit = False

    @staticmethod
    def _spinner():
        """
        Selects active spinner char
        :return:
        """
        while True:
            for cursor in '|/-\\':
                yield cursor

    def _get_color_args(self) -> list[str]:
        """
        Creates color arguments
        :return:
        """
        color_args = []
        if self._foreground_color is not None:
            color_args.append(str(self._foreground_color.value))

        if self._background_color is not None:
            color_args.append(str(self._background_color.value))

        return color_args

    def run(self) -> None:
        """
        Entry point of thread, shows the spinner
        :return:
        """
        columns = 0
        if sys.platform == 'win32':
            columns = os.get_terminal_size().columns
        else:
            term_rows, term_columns = os.popen('stty size', 'r').read().split()
            columns = int(term_columns)

        end_msg = 'done'
        end_msg_pos = columns - self._msg_len - len(end_msg)
        if end_msg_pos > 0:
            print(f'{"" : >{end_msg_pos}}', end='')
        else:
            print('', end='')

        first = True
        spinner = self._spinner()
        while self._is_spinning:
            if first:
                first = False
                print(colored(f'{next(spinner): >{len(end_msg) - 1}}', *self._get_color_args()), end='')
            else:
                print(colored(f'{next(spinner): >{len(end_msg)}}', *self._get_color_args()), end='')
            time.sleep(0.1)
            back = ''
            for i in range(0, len(end_msg)):
                back += '\b'

            print(back, end='')
            sys.stdout.flush()

        if not self._exit:
            print(colored(end_msg, *self._get_color_args()), end='')

    def stop_spinning(self):
        """
        Stops the spinner
        :return:
        """
        self._is_spinning = False
        time.sleep(0.1)

    def exit(self):
        """
        Stops the spinner
        :return:
        """
        self._is_spinning = False
        self._exit = True
        time.sleep(0.1)
