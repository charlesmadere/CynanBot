from .absSteps import AbsSteps
from .cutenessStep import CutenessStep
from .stepResult import StepResult


class CutenessSteps(AbsSteps):

    def __init__(self):
        self.__step = CutenessStep.MINUTES_BETWEEN

    def getStep(self) -> SuperTriviaStep:
        return self.__step

    def stepForward(self) -> StepResult:
        currentStep = self.__step

        match currentStep:
            case CutenessStep.MINUTES_BETWEEN:
                return StepResult.DONE

            case _:
                raise RuntimeError(f'unknown next CutenessStep: \"{currentStep}\"')
