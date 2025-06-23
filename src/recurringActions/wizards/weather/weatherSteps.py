from .weatherStep import WeatherStep
from ..absSteps import AbsSteps
from ..stepResult import StepResult
from ...actions.recurringActionType import RecurringActionType


class WeatherSteps(AbsSteps):

    def __init__(self):
        self.__step = WeatherStep.MINUTES_BETWEEN

    @property
    def currentStep(self) -> WeatherStep:
        return self.__step

    @property
    def recurringActionType(self) -> RecurringActionType:
        return RecurringActionType.WEATHER

    def stepForward(self) -> StepResult:
        currentStep = self.__step

        match currentStep:
            case WeatherStep.MINUTES_BETWEEN:
                self.__step = WeatherStep.ALERTS_ONLY
                return StepResult.NEXT

            case WeatherStep.ALERTS_ONLY:
                return StepResult.DONE

            case _:
                raise RuntimeError(f'unknown next WeatherStep: \"{currentStep}\"')
