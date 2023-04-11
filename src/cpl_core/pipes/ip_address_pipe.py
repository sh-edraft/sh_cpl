from cpl_core.pipes.pipe_abc import PipeABC


class IPAddressPipe(PipeABC):
    def __init__(self):
        pass

    def transform(self, value: list[int], *args):
        string = ""

        if len(value) != 4:
            raise Exception("Invalid IP")

        for i in range(0, len(value)):
            byte = value[i]
            if byte > 255 or byte < 0:
                raise Exception("Invalid IP")

            if i == len(value) - 1:
                string += f"{byte}"
            else:
                string += f"{byte}."

        return string
