from enum import Enum, auto

import CynanBot.misc.utils as utils


class CheerActionRequirement(Enum):

    EXACT = auto()
    GREATER_THAN_OR_EQUAL_TO = auto()

    @classmethod
    def fromStr(cls, text: str):
        if not utils.isValidStr(text):
            raise ValueError(f'text argument is malformed: \"{text}\"')

        text = text.lower()

        if text == 'exact':
            return CheerActionRequirement.EXACT
        elif text == 'greater_than_or_equal_to':
            return CheerActionRequirement.GREATER_THAN_OR_EQUAL_TO
        else:
            raise ValueError(f'unknown CheerActionRequirement: \"{text}\"')

    def toStr(self) -> str:
        if self is CheerActionRequirement.EXACT:
            return 'exact'
        elif self is CheerActionRequirement.GREATER_THAN_OR_EQUAL_TO:
            return 'greater_than_or_equal_to'
        else:
            raise RuntimeError(f'unknown CheerActionRequirement: \"{self}\"')
