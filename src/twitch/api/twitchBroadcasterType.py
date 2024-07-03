from enum import Enum, auto


class TwitchBroadcasterType(Enum):

    AFFILIATE = auto()
    NORMAL = auto()
    PARTNER = auto()

    def __repr__(self) -> str:
        match self:
            case TwitchBroadcasterType.AFFILIATE: return 'affiliate'
            case TwitchBroadcasterType.NORMAL: return 'normal'
            case TwitchBroadcasterType.PARTNER: return 'partner'
            case _: raise RuntimeError(f'unknown TwitchBroadcasterType: \"{self}\"')
