from enum import Enum, auto

import CynanBot.misc.utils as utils


class CheerActionType(Enum):

    TIMEOUT = auto()

    @classmethod
    def fromStr(cls, text: str):
        if not utils.isValidStr(text):
            raise ValueError(f'text argument is malformed: \"{text}\"')

        text = text.lower()

        if text == 'timeout':
            return CheerActionType.TIMEOUT
        else:
            raise ValueError(f'unknown CheerActionType: \"{text}\"')

    def toStr(self) -> str:
        if self is CheerActionType.TIMEOUT:
            return 'timeout'
        else:
            raise RuntimeError(f'unknown CheerActionType: \"{self}\"')
