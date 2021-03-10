import sys
import threading
import time

from termcolor import colored

from cpl.console.background_color import BackgroundColor
from cpl.console.foreground_color import ForegroundColor


class SpinnerThread(threading.Thread):

    def __init__(self, foreground_color: ForegroundColor, background_color: BackgroundColor):
        threading.Thread.__init__(self)

        self._is_spinning = True
        self._foreground_color = foreground_color
        self._background_color = background_color

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
        print('\t', end='')
        spinner = self._spinner()
        while self._is_spinning:
            print(colored(next(spinner), *self._get_color_args()), end='')
            time.sleep(0.1)
            print('\b', end='')
            sys.stdout.flush()

        print(colored('done', *self._get_color_args()), end='')

    def stop_spinning(self):
        self._is_spinning = False
        time.sleep(0.1)
