from .wordOfTheDayStep import WordOfTheDayStep
from ..absSteps import AbsSteps
from ..stepResult import StepResult
from ...actions.recurringActionType import RecurringActionType


class WordOfTheDaySteps(AbsSteps):

    def __init__(self):
        self.__step = WordOfTheDayStep.MINUTES_BETWEEN

    @property
    def currentStep(self) -> WordOfTheDayStep:
        return self.__step

    @property
    def recurringActionType(self) -> RecurringActionType:
        return RecurringActionType.WORD_OF_THE_DAY

    def stepForward(self) -> StepResult:
        currentStep = self.__step

        match currentStep:
            case WordOfTheDayStep.MINUTES_BETWEEN:
                return StepResult.DONE

            case _:
                raise RuntimeError(f'unknown next WordOfTheDayStep: \"{currentStep}\"')
