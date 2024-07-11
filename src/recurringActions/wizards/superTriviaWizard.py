from typing import Any

from .absWizard import AbsWizard
from .superTriviaSteps import SuperTriviaSteps
from ..recurringActionType import RecurringActionType
from ...misc import utils as utils


class SuperTriviaWizard(AbsWizard):

    def __init__(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ):
        super().__init__(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        self.__steps = SuperTriviaSteps()
        self.__minutesBetween: int | None = None

    def getSteps(self) -> SuperTriviaSteps:
        return self.__steps

    def printOut(self) -> str:
        return f'{self.__minutesBetween=}'

    @property
    def recurringActionType(self) -> RecurringActionType:
        return RecurringActionType.SUPER_TRIVIA

    def requireMinutesBetween(self) -> int | None:
        minutesBetween = self.__minutesBetween

        if minutesBetween is None:
            raise ValueError(f'minutesBetween value has not been set: ({self=})')

        return minutesBetween

    def setMinutesBetween(self, minutesBetween: int):
        if not utils.isValidInt(minutesBetween):
            raise TypeError(f'minutesBetween argument is malformed: \"{minutesBetween}\"')
        elif minutesBetween < 1 or minutesBetween > utils.getIntMaxSafeSize():
            raise ValueError(f'minutesBetween argument is out of bounds: {minutesBetween}')

        self.__minutesBetween = minutesBetween

    def toDictionary(self) -> dict[str, Any]:
        return {
            'minutesBetween': self.__minutesBetween,
            'recurringActionType': self.recurringActionType,
            'steps': self.__steps,
            'twitchChannel': self.twitchChannel,
            'twitchChannelId': self.twitchChannelId
        }
