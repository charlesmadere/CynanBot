from enum import Enum, auto

import CynanBot.misc.utils as utils


class RecurringActionType(Enum):

    SUPER_TRIVIA = auto()
    WEATHER = auto()
    WORD_OF_THE_DAY = auto()

    @classmethod
    def fromStr(cls, text: str):
        if not utils.isValidStr(text):
            raise ValueError(f'text argument is malformed: \"{text}\"')

        text = text.lower()

        if text in ('supertrivia', 'super_trivia'):
            return RecurringActionType.SUPER_TRIVIA
        elif text == 'weather':
            return RecurringActionType.WEATHER
        elif text in ('word', 'wordoftheday', 'word_of_the_day', 'wotd'):
            return RecurringActionType.WORD_OF_THE_DAY
        else:
            raise ValueError(f'unknown RecurringActionType: \"{text}\"')

    def getDefaultRecurringActionTimingMinutes(self) -> int:
        if self is RecurringActionType.SUPER_TRIVIA:
            return 60
        elif self is RecurringActionType.WEATHER:
            return 150
        elif self is RecurringActionType.WORD_OF_THE_DAY:
            return 90
        else:
            raise RuntimeError(f'unknown RecurringActionType: \"{self}\"')

    def getMinimumRecurringActionTimingMinutes(self) -> int:
        if self is RecurringActionType.SUPER_TRIVIA:
            return 5
        elif self is RecurringActionType.WEATHER:
            return 30
        elif self is RecurringActionType.WORD_OF_THE_DAY:
            return 30
        else:
            raise RuntimeError(f'unknown RecurringActionType: \"{self}\"')

    def toReadableStr(self) -> str:
        if self is RecurringActionType.SUPER_TRIVIA:
            return 'Super Trivia'
        elif self is RecurringActionType.WEATHER:
            return 'Weather'
        elif self is RecurringActionType.WORD_OF_THE_DAY:
            return 'Word of the Day'
        else:
            raise RuntimeError(f'unknown RecurringActionType: \"{self}\"')

    def toStr(self) -> str:
        if self is RecurringActionType.SUPER_TRIVIA:
            return 'super_trivia'
        elif self is RecurringActionType.WEATHER:
            return 'weather'
        elif self is RecurringActionType.WORD_OF_THE_DAY:
            return 'word_of_the_day'
        else:
            raise RuntimeError(f'unknown RecurringActionType: \"{self}\"')
