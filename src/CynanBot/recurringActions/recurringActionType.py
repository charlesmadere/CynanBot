from enum import Enum, auto

import CynanBot.misc.utils as utils


class RecurringActionType(Enum):

    SUPER_TRIVIA = auto()
    WEATHER = auto()
    WORD_OF_THE_DAY = auto()

    @classmethod
    def fromStr(cls, text: str):
        if not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: \"{text}\"')

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
        match self:
            case RecurringActionType.SUPER_TRIVIA: return 60
            case RecurringActionType.WEATHER: return 150
            case RecurringActionType.WORD_OF_THE_DAY: return 90
            case _: raise RuntimeError(f'unknown RecurringActionType: \"{self}\"')

    def getMinimumRecurringActionTimingMinutes(self) -> int:
        match self:
            case RecurringActionType.SUPER_TRIVIA: return 5
            case RecurringActionType.WEATHER: return 30
            case RecurringActionType.WORD_OF_THE_DAY: return 30
            case _: raise RuntimeError(f'unknown RecurringActionType: \"{self}\"')

    def __repr__(self) -> str:
        return self.toStr()

    def toReadableStr(self) -> str:
        match self:
            case RecurringActionType.SUPER_TRIVIA: return 'Super Trivia'
            case RecurringActionType.WEATHER: return 'Weather'
            case RecurringActionType.WORD_OF_THE_DAY: return 'Word of the Day'
            case _: raise RuntimeError(f'unknown RecurringActionType: \"{self}\"')

    def toStr(self) -> str:
        match self:
            case RecurringActionType.SUPER_TRIVIA: return 'super_trivia'
            case RecurringActionType.WEATHER: return 'weather'
            case RecurringActionType.WORD_OF_THE_DAY: return 'word_of_the_day'
            case _: raise RuntimeError(f'unknown RecurringActionType: \"{self}\"')
