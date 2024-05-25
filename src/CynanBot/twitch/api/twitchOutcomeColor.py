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

        match text:
            case 'blue': return TwitchOutcomeColor.BLUE
            case 'pink': return TwitchOutcomeColor.PINK
            case _: raise ValueError(f'unknown TwitchOutcomeColor: \"{text}\"')
