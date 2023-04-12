from cpl_cli.configuration import VersionSettingsNameEnum
from cpl_core.pipes.pipe_abc import PipeABC


class VersionPipe(PipeABC):
    def __init__(self):
        pass

    def transform(self, value: dict, *args):
        for atr in VersionSettingsNameEnum:
            if atr.value not in value:
                raise KeyError(atr.value)

        v_str = f"{value[VersionSettingsNameEnum.major.value]}.{value[VersionSettingsNameEnum.minor.value]}"
        if value[VersionSettingsNameEnum.micro.value] is not None:
            v_str += f".{value[VersionSettingsNameEnum.micro.value]}"
        return v_str
