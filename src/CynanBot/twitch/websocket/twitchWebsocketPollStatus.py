from enum import Enum, auto
from typing import Optional

import CynanBot.misc.utils as utils


class TwitchWebsocketPollStatus(Enum):

    ARCHIVED = auto()
    COMPLETED = auto()
    TERMINATED = auto()

    @classmethod
    def fromStr(cls, text: Optional[str]):
        if not utils.isValidStr(text):
            return None

        text = text.lower()

        if text == 'archived':
            return TwitchWebsocketPollStatus.ARCHIVED
        elif text == 'completed':
            return TwitchWebsocketPollStatus.COMPLETED
        elif text == 'terminated':
            return TwitchWebsocketPollStatus.TERMINATED
        else:
            return None
