from .voicemailStep import VoicemailStep
from ..absSteps import AbsSteps
from ..stepResult import StepResult


class VoicemailSteps(AbsSteps):

    def __init__(self):
        self.__step = VoicemailStep.BITS

    def getStep(self) -> VoicemailStep:
        return self.__step

    def stepForward(self) -> StepResult:
        currentStep = self.__step

        match currentStep:
            case VoicemailStep.BITS:
                return StepResult.DONE

            case _:
                raise RuntimeError(f'unknown next VoicemailStep: \"{currentStep}\"')
