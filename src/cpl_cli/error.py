from cpl.console.console import Console


class Error:

    @staticmethod
    def error(message: str):
        Console.error(message)
        Console.error('Run \'cpl help\'')
