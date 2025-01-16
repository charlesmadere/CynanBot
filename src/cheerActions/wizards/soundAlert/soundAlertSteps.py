from .soundAlertStep import SoundAlertStep
from ..absSteps import AbsSteps
from ..stepResult import StepResult


class SoundAlertSteps(AbsSteps):

    def __init__(self):
        self.__step = SoundAlertStep.BITS

    def getStep(self) -> SoundAlertStep:
        return self.__step

    def stepForward(self) -> StepResult:
        currentStep = self.__step

        match currentStep:
            case SoundAlertStep.BITS:
                self.__step = SoundAlertStep.DIRECTORY
                return StepResult.NEXT

            case SoundAlertStep.DIRECTORY:
                return StepResult.DONE

            case _:
                raise RuntimeError(f'unknown next SoundAlertStep: \"{currentStep}\"')
