from enum import Enum, auto


class TwitchUserType(Enum):

    ADMIN = auto()
    GLOBAL_MOD = auto()
    NORMAL = auto()
    STAFF = auto()

    def toStr(self) -> str:
        match self:
            case TwitchUserType.ADMIN: return 'admin'
            case TwitchUserType.GLOBAL_MOD: return 'global_mod'
            case TwitchUserType.NORMAL: return 'normal'
            case TwitchUserType.STAFF: return 'staff'
            case _: raise RuntimeError(f'unknown TwitchUserType: \"{self}\"')
