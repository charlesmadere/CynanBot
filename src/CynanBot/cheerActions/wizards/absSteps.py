from abc import ABC, abstractmethod

from CynanBot.cheerActions.wizards.absStep import AbsStep
from CynanBot.cheerActions.wizards.stepResult import StepResult


class AbsSteps(ABC):

    @abstractmethod
    def getStep(self) -> AbsStep:
        pass

    @abstractmethod
    def stepForward(self) -> StepResult:
        pass
