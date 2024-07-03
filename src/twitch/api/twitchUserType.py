from enum import Enum, auto

from ...misc import utils as utils


class TwitchUserType(Enum):

    ADMIN = auto()
    GLOBAL_MOD = auto()
    NORMAL = auto()
    STAFF = auto()

    @classmethod
    def fromStr(cls, text: str | None):
        if not utils.isValidStr(text):
            return TwitchUserType.NORMAL

        text = text.lower()

        match text:
            case 'admin': return TwitchUserType.ADMIN
            case 'global_mod': return TwitchUserType.GLOBAL_MOD
            case 'staff': return TwitchUserType.STAFF
            case _: return TwitchUserType.NORMAL

    def __str__(self) -> str:
        match self:
            case TwitchUserType.ADMIN: return 'admin'
            case TwitchUserType.GLOBAL_MOD: return 'global_mod'
            case TwitchUserType.NORMAL: return 'normal'
            case TwitchUserType.STAFF: return 'staff'
            case _: raise RuntimeError(f'unknown TwitchUserType: \"{self}\"')
