from CynanBot.recurringActions.recurringActionType import RecurringActionType
from CynanBot.recurringActions.wizards.absWizard import AbsWizard
from CynanBot.recurringActions.wizards.weatherSteps import WeatherSteps


class WeatherWizard(AbsWizard):

    def __init__(self):
        self.__steps = WeatherSteps()

    def getRecurringActionType(self) -> RecurringActionType:
        return RecurringActionType.WEATHER

    def getSteps(self) -> WeatherSteps:
        return self.__steps
