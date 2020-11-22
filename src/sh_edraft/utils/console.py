from termcolor import colored


class Console:

    @staticmethod
    def write_line(string: str, color: str = None):
        if color is not None:
            print(colored(string, color))
        else:
            print(string)
