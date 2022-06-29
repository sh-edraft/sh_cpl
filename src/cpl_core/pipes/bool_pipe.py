from cpl_core.pipes.pipe_abc import PipeABC


class BoolPipe(PipeABC):

    def __init__(self): pass

    def transform(self, value: bool, *args):
        return 'True' if value else 'False'
