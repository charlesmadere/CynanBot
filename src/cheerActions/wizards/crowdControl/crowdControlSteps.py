from .crowdControlStep import CrowdControlStep
from ..absSteps import AbsSteps
from ..stepResult import StepResult
from ...cheerActionType import CheerActionType


class CrowdControlSteps(AbsSteps):

    def __init__(self):
        self.__step = CrowdControlStep.BITS

    @property
    def cheerActionType(self) -> CheerActionType:
        return CheerActionType.CROWD_CONTROL

    @property
    def currentStep(self) -> CrowdControlStep:
        return self.__step

    def stepForward(self) -> StepResult:
        currentStep = self.__step

        match currentStep:
            case CrowdControlStep.BITS:
                return StepResult.DONE

            case _:
                raise RuntimeError(f'unknown next CrowdControlStep: \"{currentStep}\"')
