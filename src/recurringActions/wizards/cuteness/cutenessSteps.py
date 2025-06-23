from .cutenessStep import CutenessStep
from ..absSteps import AbsSteps
from ..stepResult import StepResult
from ...actions.recurringActionType import RecurringActionType


class CutenessSteps(AbsSteps):

    def __init__(self):
        self.__step = CutenessStep.MINUTES_BETWEEN

    @property
    def currentStep(self) -> CutenessStep:
        return self.__step

    @property
    def recurringActionType(self) -> RecurringActionType:
        return RecurringActionType.CUTENESS

    def stepForward(self) -> StepResult:
        currentStep = self.__step

        match currentStep:
            case CutenessStep.MINUTES_BETWEEN:
                return StepResult.DONE

            case _:
                raise RuntimeError(f'unknown next CutenessStep: \"{currentStep}\"')
