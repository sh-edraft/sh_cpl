from cpl.console.console import Console

from model.test_model import TestModel


def main():
    Console.write_line('Hello World')
    Console.write_line('Dies ist ein test')
    test = TestModel()


if __name__ == '__main__':
    main()
