from typing import Any, Final

from .superTriviaStep import SuperTriviaStep
from .superTriviaSteps import SuperTriviaSteps
from ..absWizard import AbsWizard
from ...actions.recurringActionType import RecurringActionType
from ....misc import utils as utils


class SuperTriviaWizard(AbsWizard):

    def __init__(
        self,
        twitchChannel: str,
        twitchChannelId: str,
    ):
        super().__init__(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
        )

        self.__steps: Final[SuperTriviaSteps] = SuperTriviaSteps()
        self.__minutesBetween: int | None = None

    @property
    def currentStep(self) -> SuperTriviaStep:
        return self.__steps.currentStep

    def printOut(self) -> str:
        return f'{self.__minutesBetween=}'

    @property
    def recurringActionType(self) -> RecurringActionType:
        return RecurringActionType.SUPER_TRIVIA

    def requireMinutesBetween(self) -> int:
        minutesBetween = self.__minutesBetween

        if minutesBetween is None:
            raise ValueError(f'minutesBetween value has not been set: ({self=})')

        return minutesBetween

    def setMinutesBetween(self, minutesBetween: int):
        if not utils.isValidInt(minutesBetween):
            raise TypeError(f'minutesBetween argument is malformed: \"{minutesBetween}\"')
        elif minutesBetween < 1 or minutesBetween > utils.getIntMaxSafeSize():
            raise ValueError(f'minutesBetween argument is out of bounds: {minutesBetween}')
        elif minutesBetween < self.recurringActionType.minimumRecurringActionTimingMinutes:
            raise ValueError(f'minutesBetween argument is below the minimum requirement: {minutesBetween}')

        self.__minutesBetween = minutesBetween

    @property
    def steps(self) -> SuperTriviaSteps:
        return self.__steps

    def toDictionary(self) -> dict[str, Any]:
        return {
            'currentStep': self.currentStep,
            'minutesBetween': self.__minutesBetween,
            'recurringActionType': self.recurringActionType,
            'steps': self.__steps,
            'twitchChannel': self.twitchChannel,
            'twitchChannelId': self.twitchChannelId,
        }
