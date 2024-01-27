from enum import Enum, auto
from typing import Optional

import CynanBot.misc.utils as utils


class TwitchWebsocketPollStatus(Enum):

    ACTIVE = auto()
    ARCHIVED = auto()
    COMPLETED = auto()
    INVALID = auto()
    MODERATED = auto()
    TERMINATED = auto()

    @classmethod
    def fromStr(cls, text: Optional[str]):
        if not utils.isValidStr(text):
            return None

        text = text.lower()

        if text == 'active':
            return TwitchWebsocketPollStatus.ACTIVE
        elif text == 'archived':
            return TwitchWebsocketPollStatus.ARCHIVED
        elif text == 'completed':
            return TwitchWebsocketPollStatus.COMPLETED
        elif text == 'invalid':
            return TwitchWebsocketPollStatus.INVALID
        elif text == 'moderated':
            return TwitchWebsocketPollStatus.MODERATED
        elif text == 'terminated':
            return TwitchWebsocketPollStatus.TERMINATED
        else:
            return None
