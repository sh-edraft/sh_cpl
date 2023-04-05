from enum import Enum


class ProjectTypeEnum(Enum):
    console = "console"
    library = "library"
    unittest = "unittest"
    discord_bot = "discord-bot"
