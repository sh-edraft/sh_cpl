from cpl_core.pipes.pipe_abc import PipeABC


class FirstCharToLowerPipe(PipeABC):

    def __init__(self): pass

    def transform(self, value: any, *args):
        return f'{value[0].lower()}{value[1:]}'
