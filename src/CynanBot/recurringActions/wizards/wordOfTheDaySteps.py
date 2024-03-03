from CynanBot.recurringActions.wizards.absSteps import AbsSteps
from CynanBot.recurringActions.wizards.stepResult import StepResult
from CynanBot.recurringActions.wizards.wordOfTheDayStep import WordOfTheDayStep


class WordOfTheDaySteps(AbsSteps):

    def __init__(self):
        self.__step = WordOfTheDayStep.MINUTES_BETWEEN

    def getStep(self) -> WordOfTheDayStep:
        return self.__step

    def stepForward(self) -> StepResult:
        if self.__step is WordOfTheDayStep.MINUTES_BETWEEN:
            return StepResult.DONE
        else:
            raise RuntimeError(f'unknown WordOfTheDayStep: \"{self.__step}\"')
