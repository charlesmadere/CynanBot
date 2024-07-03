from .absSteps import AbsSteps
from .stepResult import StepResult
from .weatherStep import WeatherStep


class WeatherSteps(AbsSteps):

    def __init__(self):
        self.__step = WeatherStep.MINUTES_BETWEEN

    def getStep(self) -> WeatherStep:
        return self.__step

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
