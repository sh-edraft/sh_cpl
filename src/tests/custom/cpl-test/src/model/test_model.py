import time

from cpl.console import Console


class TestModel:

    def __init__(self):
        Console.spinner('Waiting: ', self._wait, 3)
        option = Console.select('->', 'Select option: ', [
            'Option 1',
            'Option 2',
            'Option 3',
            'Option 4',
            'Option 5',
            'Option 6'
        ])
        Console.write_line('You selected', option)

    @staticmethod
    def _wait(count: int):
        time.sleep(count)
