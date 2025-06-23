from .soundAlertStep import SoundAlertStep
from ..absSteps import AbsSteps
from ..stepResult import StepResult
from ...cheerActionType import CheerActionType


class SoundAlertSteps(AbsSteps):

    def __init__(self):
        self.__step = SoundAlertStep.BITS

    @property
    def cheerActionType(self) -> CheerActionType:
        return CheerActionType.SOUND_ALERT

    @property
    def currentStep(self) -> SoundAlertStep:
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
