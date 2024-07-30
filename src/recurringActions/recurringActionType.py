from enum import Enum, auto


class RecurringActionType(Enum):

    CUTENESS = auto()
    SUPER_TRIVIA = auto()
    WEATHER = auto()
    WORD_OF_THE_DAY = auto()

    def getDefaultRecurringActionTimingMinutes(self) -> int:
        match self:
            case RecurringActionType.CUTENESS: return 120
            case RecurringActionType.SUPER_TRIVIA: return 60
            case RecurringActionType.WEATHER: return 150
            case RecurringActionType.WORD_OF_THE_DAY: return 90
            case _: raise RuntimeError(f'unknown RecurringActionType: \"{self}\"')

    @property
    def minimumRecurringActionTimingMinutes(self) -> int:
        match self:
            case RecurringActionType.CUTENESS: return 30
            case RecurringActionType.SUPER_TRIVIA: return 5
            case RecurringActionType.WEATHER: return 30
            case RecurringActionType.WORD_OF_THE_DAY: return 30
            case _: raise RuntimeError(f'unknown RecurringActionType: \"{self}\"')

    def toReadableStr(self) -> str:
        match self:
            case RecurringActionType.CUTENESS: return 'Cuteness'
            case RecurringActionType.SUPER_TRIVIA: return 'Super Trivia'
            case RecurringActionType.WEATHER: return 'Weather'
            case RecurringActionType.WORD_OF_THE_DAY: return 'Word of the Day'
            case _: raise RuntimeError(f'unknown RecurringActionType: \"{self}\"')
