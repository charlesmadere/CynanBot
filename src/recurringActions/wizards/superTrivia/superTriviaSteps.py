from .superTriviaStep import SuperTriviaStep
from ..absSteps import AbsSteps
from ..stepResult import StepResult
from ...actions.recurringActionType import RecurringActionType


class SuperTriviaSteps(AbsSteps):

    def __init__(self):
        self.__step = SuperTriviaStep.MINUTES_BETWEEN

    @property
    def currentStep(self) -> SuperTriviaStep:
        return self.__step

    @property
    def recurringActionType(self) -> RecurringActionType:
        return RecurringActionType.SUPER_TRIVIA

    def stepForward(self) -> StepResult:
        currentStep = self.__step

        match currentStep:
            case SuperTriviaStep.MINUTES_BETWEEN:
                return StepResult.DONE

            case _:
                raise RuntimeError(f'unknown next SuperTriviaStep: \"{currentStep}\"')
