import time
from cpl.console import Console, ForegroundColorEnum


def test_spinner():
    time.sleep(2)


def test_console():
    Console.write_line('Hello World')
    Console.write('\nName: ')
    Console.write_line(' Hello', Console.read_line())
    Console.clear()
    Console.write_at(5, 5, 'at 5, 5')
    Console.write_at(10, 10, 'at 10, 10')


if __name__ == '__main__':
    Console.write_line('Hello World\n')
    Console.spinner('Test:', test_spinner, spinner_foreground_color=ForegroundColorEnum.cyan,
                    text_foreground_color='green')
    # opts = [
    #     'Option 1',
    #     'Option 2',
    #     'Option 3',
    #     'Option 4'
    # ]
    # selected = Console.select(
    #     '>',
    #     'Select item:',
    #     opts,
    #     header_foreground_color=ForegroundColorEnum.blue,
    #     option_foreground_color=ForegroundColorEnum.green,
    #     cursor_foreground_color=ForegroundColorEnum.red
    # )
    # Console.write_line(f'You selected: {selected}')
    # test_console()

    Console.write_line()
