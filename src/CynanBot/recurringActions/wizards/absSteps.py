from abc import ABC, abstractmethod
from typing import Any

from CynanBot.recurringActions.wizards.absStep import AbsStep
from CynanBot.recurringActions.wizards.stepResult import StepResult


class AbsSteps(ABC):

    @abstractmethod
    def getStep(self) -> AbsStep:
        pass

    @abstractmethod
    def stepForward(self) -> StepResult:
        pass

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'step': self.getStep()
        }
