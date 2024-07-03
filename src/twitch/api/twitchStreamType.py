from enum import Enum, auto

from ...misc import utils as utils


class TwitchStreamType(Enum):

    LIVE = auto()
    UNKNOWN = auto()

    @classmethod
    def fromStr(cls, text: str | None):
        if not utils.isValidStr(text):
            return TwitchStreamType.UNKNOWN

        text = text.lower()

        match text:
            case 'live': return TwitchStreamType.LIVE
            case _: return TwitchStreamType.UNKNOWN
