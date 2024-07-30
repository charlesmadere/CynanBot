from typing import Any

from .absWizard import AbsWizard
from .wordOfTheDaySteps import WordOfTheDaySteps
from ..recurringActionType import RecurringActionType
from ...misc import utils as utils


class WordOfTheDayWizard(AbsWizard):

    def __init__(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ):
        super().__init__(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        self.__steps = WordOfTheDaySteps()
        self.__minutesBetween: int | None = None

    def getMinutesBetween(self) -> int | None:
        return self.__minutesBetween

    def getSteps(self) -> WordOfTheDaySteps:
        return self.__steps

    def printOut(self) -> str:
        return f'{self.__minutesBetween=}'

    @property
    def recurringActionType(self) -> RecurringActionType:
        return RecurringActionType.WORD_OF_THE_DAY

    def setMinutesBetween(self, minutesBetween: int):
        if not utils.isValidInt(minutesBetween):
            raise TypeError(f'minutesBetween argument is malformed: \"{minutesBetween}\"')
        elif minutesBetween < 1 or minutesBetween > utils.getIntMaxSafeSize():
            raise ValueError(f'minutesBetween argument is out of bounds: {minutesBetween}')
        elif minutesBetween < self.recurringActionType.minimumRecurringActionTimingMinutes:
            raise ValueError(f'minutesBetween argument is below the minimum requirement: {minutesBetween}')

        self.__minutesBetween = minutesBetween

    def toDictionary(self) -> dict[str, Any]:
        return {
            'minutesBetween': self.__minutesBetween,
            'recurringActionType': self.recurringActionType,
            'steps': self.__steps,
            'twitchChannel': self.twitchChannel,
            'twitchChannelId': self.twitchChannelId
        }
