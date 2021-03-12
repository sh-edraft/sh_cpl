import os
import sys
import threading
import time

from termcolor import colored

from cpl.console.background_color_enum import BackgroundColorEnum
from cpl.console.foreground_color_enum import ForegroundColor


class SpinnerThread(threading.Thread):

    def __init__(self, msg_len: int, foreground_color: ForegroundColor, background_color: BackgroundColorEnum):
        threading.Thread.__init__(self)

        self._msg_len = msg_len
        self._foreground_color = foreground_color
        self._background_color = background_color

        self._is_spinning = True

    @staticmethod
    def _spinner():
        while True:
            for cursor in '|/-\\':
                yield cursor

    def _get_color_args(self) -> list[str]:
        color_args = []
        if self._foreground_color is not None:
            color_args.append(str(self._foreground_color.value))

        if self._background_color is not None:
            color_args.append(str(self._background_color.value))

        return color_args

    def run(self) -> None:
        rows, columns = os.popen('stty size', 'r').read().split()
        end_msg = 'done'
        columns = int(columns) - self._msg_len - len(end_msg)
        print(f'{"" : >{columns}}', end='')
        spinner = self._spinner()
        while self._is_spinning:
            print(colored(f'{next(spinner): >{len(end_msg)}}', *self._get_color_args()), end='')
            time.sleep(0.1)
            back = ''
            for i in range(0, len(end_msg)):
                back += '\b'

            print(back, end='')
            sys.stdout.flush()

        print(colored(end_msg, *self._get_color_args()), end='')

    def stop_spinning(self):
        self._is_spinning = False
        time.sleep(0.1)
