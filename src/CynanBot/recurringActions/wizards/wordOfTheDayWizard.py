from CynanBot.recurringActions.recurringActionType import RecurringActionType
from CynanBot.recurringActions.wizards.absWizard import AbsWizard
from CynanBot.recurringActions.wizards.wordOfTheDaySteps import \
    WordOfTheDaySteps


class WordOfTheDayWizard(AbsWizard):

    def __init__(self):
        self.__steps = WordOfTheDaySteps()

    def getRecurringActionType(self) -> RecurringActionType:
        return RecurringActionType.WORD_OF_THE_DAY

    def getSteps(self) -> WordOfTheDaySteps:
        return self.__steps
