from .tntTimeoutStep import TntTimeoutStep
from ..absSteps import AbsSteps
from ..stepResult import StepResult


class TntTimeoutSteps(AbsSteps):

    def __init__(self):
        self.__step = TntTimeoutStep.BITS

    def getStep(self) -> TntTimeoutStep:
        return self.__step

    def stepForward(self) -> StepResult:
        currentStep = self.__step

        match currentStep:
            case TntTimeoutStep.BITS:
                self.__step = TntTimeoutStep.DURATION_SECONDS
                return StepResult.NEXT

            case TntTimeoutStep.DURATION_SECONDS:
                self.__step = TntTimeoutStep.MINIMUM_CHATTERS
                return StepResult.NEXT

            case TntTimeoutStep.MAXIMUM_CHATTERS:
                return StepResult.DONE

            case TntTimeoutStep.MINIMUM_CHATTERS:
                self.__step = TntTimeoutStep.MAXIMUM_CHATTERS
                return StepResult.NEXT

            case _:
                raise RuntimeError(f'unknown next TntTimeoutStep: \"{currentStep}\"')
