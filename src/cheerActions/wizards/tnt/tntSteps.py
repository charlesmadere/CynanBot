from .tntStep import TntStep
from ..absSteps import AbsSteps
from ..stepResult import StepResult


class TntSteps(AbsSteps):

    def __init__(self):
        self.__step = TntStep.BITS

    def getStep(self) -> TntStep:
        return self.__step

    def stepForward(self) -> StepResult:
        currentStep = self.__step

        match currentStep:
            case TntStep.BITS:
                self.__step = TntStep.MINIMUM_DURATION_SECONDS
                return StepResult.NEXT

            case TntStep.MAXIMUM_CHATTERS:
                return StepResult.DONE

            case TntStep.MAXIMUM_DURATION_SECONDS:
                self.__step = TntStep.MINIMUM_CHATTERS
                return StepResult.NEXT

            case TntStep.MINIMUM_CHATTERS:
                self.__step = TntStep.MAXIMUM_CHATTERS
                return StepResult.NEXT

            case TntStep.MINIMUM_DURATION_SECONDS:
                self.__step = TntStep.MAXIMUM_DURATION_SECONDS
                return StepResult.NEXT

            case _:
                raise RuntimeError(f'unknown next TntTimeoutStep: \"{currentStep}\"')
