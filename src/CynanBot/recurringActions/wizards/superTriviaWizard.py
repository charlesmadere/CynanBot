from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.recurringActions.recurringActionType import RecurringActionType
from CynanBot.recurringActions.wizards.absWizard import AbsWizard
from CynanBot.recurringActions.wizards.superTriviaSteps import SuperTriviaSteps


class SuperTriviaWizard(AbsWizard):

    def __init__(self):
        self.__steps = SuperTriviaSteps()
        self.__minutesBetween: Optional[int] = None

    def getRecurringActionType(self) -> RecurringActionType:
        return RecurringActionType.SUPER_TRIVIA

    def getSteps(self) -> SuperTriviaSteps:
        return self.__steps

    def setMinutesBetween(self, minutesBetween: int):
        if not utils.isValidInt(minutesBetween):
            raise TypeError(f'minutesBetween argument is malformed: \"{minutesBetween}\"')

        self.__minutesBetween = minutesBetween
