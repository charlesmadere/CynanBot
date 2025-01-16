from .cutenessStep import CutenessStep
from ..absSteps import AbsSteps
from ..stepResult import StepResult


class CutenessSteps(AbsSteps):

    def __init__(self):
        self.__step = CutenessStep.MINUTES_BETWEEN

    def getStep(self) -> CutenessStep:
        return self.__step

    def stepForward(self) -> StepResult:
        currentStep = self.__step

        match currentStep:
            case CutenessStep.MINUTES_BETWEEN:
                return StepResult.DONE

            case _:
                raise RuntimeError(f'unknown next CutenessStep: \"{currentStep}\"')
