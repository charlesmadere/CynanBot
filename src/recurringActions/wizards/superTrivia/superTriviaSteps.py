from .superTriviaStep import SuperTriviaStep
from ..absSteps import AbsSteps
from ..stepResult import StepResult


class SuperTriviaSteps(AbsSteps):

    def __init__(self):
        self.__step = SuperTriviaStep.MINUTES_BETWEEN

    def getStep(self) -> SuperTriviaStep:
        return self.__step

    def stepForward(self) -> StepResult:
        currentStep = self.__step

        match currentStep:
            case SuperTriviaStep.MINUTES_BETWEEN:
                return StepResult.DONE

            case _:
                raise RuntimeError(f'unknown next SuperTriviaStep: \"{currentStep}\"')
