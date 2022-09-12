from typing import Union, Sequence

from cpl_discord.container.container import Container


class ToContainersConverter:

    @staticmethod
    def convert(_l: Union[list[object], Sequence[object]], _t: type) -> list[Container]:
        values = []
        for e in _l:
            values.append(_t(e))
        return values
