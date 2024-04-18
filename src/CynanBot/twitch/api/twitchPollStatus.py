from enum import Enum, auto

import CynanBot.misc.utils as utils


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

        if text == 'active':
            return TwitchPollStatus.ACTIVE
        elif text == 'archived':
            return TwitchPollStatus.ARCHIVED
        elif text == 'completed':
            return TwitchPollStatus.COMPLETED
        elif text == 'invalid':
            return TwitchPollStatus.INVALID
        elif text == 'moderated':
            return TwitchPollStatus.MODERATED
        elif text == 'terminated':
            return TwitchPollStatus.TERMINATED
        else:
            return None
