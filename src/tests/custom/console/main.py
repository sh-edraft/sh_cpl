import time
from cpl.console import Console, ForegroundColorEnum


def test_spinner():
    time.sleep(2)


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

    Console.write_line()
