from enum import Enum, auto


class MessageMethod(Enum):

    IRC = auto()
    TWITCH_API = auto()

    def toStr(self) -> str:
        match self:
            case MessageMethod.IRC: return 'IRC'
            case MessageMethod.TWITCH_API: return 'Twitch API'
            case _: raise RuntimeError(f'unknown MessageMethod: \"{self}\"')
