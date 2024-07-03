from enum import Enum, auto

from ...misc import utils as utils


class TwitchPollStatus(Enum):

    ACTIVE = auto()
    ARCHIVED = auto()
    COMPLETED = auto()
    INVALID = auto()
    MODERATED = auto()
    TERMINATED = auto()

    @classmethod
    def fromStr(cls, text: str | None):
        if not utils.isValidStr(text):
            return None

        text = text.lower()

        match text:
            case 'active': return TwitchPollStatus.ACTIVE
            case 'archived': return TwitchPollStatus.ARCHIVED
            case 'completed': return TwitchPollStatus.COMPLETED
            case 'invalid': return TwitchPollStatus.INVALID
            case 'moderated': return TwitchPollStatus.MODERATED
            case 'terminated': return TwitchPollStatus.TERMINATED
            case _: return None
