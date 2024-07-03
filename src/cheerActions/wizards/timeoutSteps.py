from .absSteps import AbsSteps
from .stepResult import StepResult
from .timeoutStep import TimeoutStep


class TimeoutSteps(AbsSteps):

    def __init__(self):
        self.__step = TimeoutStep.BITS

    def getStep(self) -> TimeoutStep:
        return self.__step

    def stepForward(self) -> StepResult:
        currentStep = self.__step

        match currentStep:
            case TimeoutStep.BITS:
                self.__step = TimeoutStep.DURATION_SECONDS
                return StepResult.NEXT

            case TimeoutStep.DURATION_SECONDS:
                self.__step = TimeoutStep.STREAM_STATUS
                return StepResult.NEXT

            case TimeoutStep.STREAM_STATUS:
                return StepResult.DONE

            case _:
                raise RuntimeError(f'unknown next TimeoutStep: \"{currentStep}\"')
