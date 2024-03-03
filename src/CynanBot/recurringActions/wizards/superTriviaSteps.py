from CynanBot.recurringActions.wizards.absSteps import AbsSteps
from CynanBot.recurringActions.wizards.stepResult import StepResult
from CynanBot.recurringActions.wizards.superTriviaStep import SuperTriviaStep


class SuperTriviaSteps(AbsSteps):

    def __init__(self):
        self.__step = SuperTriviaStep.MINUTES_BETWEEN

    def getStep(self) -> SuperTriviaStep:
        return self.__step

    def stepForward(self) -> StepResult:
        if self.__step is SuperTriviaStep.MINUTES_BETWEEN:
            return StepResult.DONE
        else:
            raise RuntimeError(f'unknown SuperTriviaStep: \"{self.__step}\"')
