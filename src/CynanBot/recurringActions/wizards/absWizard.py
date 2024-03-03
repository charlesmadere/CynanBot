from abc import ABC, abstractmethod

from CynanBot.recurringActions.recurringActionType import RecurringActionType
from CynanBot.recurringActions.wizards.absSteps import AbsSteps


class AbsWizard(ABC):

    @abstractmethod
    def getRecurringActionType(self) -> RecurringActionType:
        pass

    @abstractmethod
    def getSteps(self) -> AbsSteps:
        pass
