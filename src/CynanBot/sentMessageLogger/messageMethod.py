from enum import Enum, auto


class MessageMethod(Enum):

    IRC = auto()
    TWITCH_API = auto()

    def toStr(self) -> str:
        if self is MessageMethod.IRC:
            return 'IRC'
        elif self is MessageMethod.TWITCH_API:
            return 'Twitch API'
        else:
            raise RuntimeError(f'unknown MessageMethod: \"{self}\"')
