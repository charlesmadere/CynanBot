from CynanBot.recurringActions.wizards.absSteps import AbsSteps
from CynanBot.recurringActions.wizards.stepResult import StepResult
from CynanBot.recurringActions.wizards.weatherStep import WeatherStep


class WeatherSteps(AbsSteps):

    def __init__(self):
        self.__step = WeatherStep.MINUTES_BETWEEN

    def getStep(self) -> WeatherStep:
        return self.__step

    def stepForward(self) -> StepResult:
        if self.__step is WeatherStep.MINUTES_BETWEEN:
            self.__step = WeatherStep.ALERTS_ONLY
            return StepResult.NEXT
        elif self.__step is WeatherStep.ALERTS_ONLY:
            return StepResult.DONE
        else:
            raise RuntimeError(f'unknown WeatherStep: \"{self.__step}\"')
