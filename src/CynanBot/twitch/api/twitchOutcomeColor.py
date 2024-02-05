from enum import Enum, auto

import CynanBot.misc.utils as utils


class TwitchOutcomeColor(Enum):

    BLUE = auto()
    PINK = auto()

    @classmethod
    def fromStr(cls, text: str):
        if not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: \"{text}\"')

        text = text.lower()

        if text == 'blue':
            return TwitchOutcomeColor.BLUE
        elif text == 'pink':
            return TwitchOutcomeColor.PINK
        else:
            raise ValueError(f'unknown TwitchOutcomeColor: \"{text}\"')
