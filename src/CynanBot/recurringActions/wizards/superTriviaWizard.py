from CynanBot.recurringActions.recurringActionType import RecurringActionType
from CynanBot.recurringActions.wizards.absWizard import AbsWizard
from CynanBot.recurringActions.wizards.superTriviaSteps import SuperTriviaSteps


class SuperTriviaWizard(AbsWizard):

    def __init__(self):
        self.__steps = SuperTriviaSteps()

    def getRecurringActionType(self) -> RecurringActionType:
        return RecurringActionType.SUPER_TRIVIA

    def getSteps(self) -> SuperTriviaSteps:
        return self.__steps
