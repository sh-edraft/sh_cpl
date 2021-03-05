import threading
import time


class SpinnerThread(threading.Thread):

    def __init__(self, console):
        threading.Thread.__init__(self)

        self._console = console
        self._is_spinning = True

    @staticmethod
    def _spinner():
        while True:
            for cursor in '|/-\\':
                yield cursor

    def run(self) -> None:
        self._console.write('\t')
        spinner = self._spinner()
        while self._is_spinning:
            self._console.write(next(spinner))
            time.sleep(0.1)
            self._console.write('\b')

            self._console.flush()

        self._console.write(' ')

    def stop_spinning(self):
        self._is_spinning = False
        time.sleep(0.1)
