from abc import ABC, abstractmethod

from CynanBot.recurringActions.wizards.absStep import AbsStep
from CynanBot.recurringActions.wizards.stepResult import StepResult


class AbsSteps(ABC):

    @abstractmethod
    def getStep(self) -> AbsStep:
        pass

    @abstractmethod
    def stepForward(self) -> StepResult:
        pass
