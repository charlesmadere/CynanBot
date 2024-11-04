from .crowdControlStep import CrowdControlStep
from ..absSteps import AbsSteps
from ..stepResult import StepResult


class CrowdControlSteps(AbsSteps):

    def __init__(self):
        self.__step = CrowdControlStep.BITS

    def getStep(self) -> CrowdControlStep:
        return self.__step

    def stepForward(self) -> StepResult:
        currentStep = self.__step

        match currentStep:
            case CrowdControlStep.BITS:
                return StepResult.DONE

            case _:
                raise RuntimeError(f'unknown next CrowdControlStep: \"{currentStep}\"')
