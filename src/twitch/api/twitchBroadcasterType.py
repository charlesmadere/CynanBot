from enum import Enum, auto

from ...misc import utils as utils


class TwitchBroadcasterType(Enum):

    AFFILIATE = auto()
    NORMAL = auto()
    PARTNER = auto()

    @classmethod
    def fromStr(cls, text: str | None):
        if not utils.isValidStr(text):
            return TwitchBroadcasterType.NORMAL

        text = text.lower()

        match text:
            case 'affiliate': return TwitchBroadcasterType.AFFILIATE
            case 'partner': return TwitchBroadcasterType.PARTNER
            case _: return TwitchBroadcasterType.NORMAL

    def __repr__(self) -> str:
        match self:
            case TwitchBroadcasterType.AFFILIATE: return 'affiliate'
            case TwitchBroadcasterType.NORMAL: return 'normal'
            case TwitchBroadcasterType.PARTNER: return 'partner'
            case _: raise RuntimeError(f'unknown TwitchBroadcasterType: \"{self}\"')
