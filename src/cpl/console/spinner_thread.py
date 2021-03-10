import sys
import threading
import time


class SpinnerThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        self._is_spinning = True

    @staticmethod
    def _spinner():
        while True:
            for cursor in '|/-\\':
                yield cursor

    def run(self) -> None:
        print('\t', end='')
        spinner = self._spinner()
        while self._is_spinning:
            print(next(spinner), end='')
            time.sleep(0.1)
            print('\b', end='')

            sys.stdout.flush()

        print('done', end='')

    def stop_spinning(self):
        self._is_spinning = False
        time.sleep(0.1)
