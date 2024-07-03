from abc import ABC, abstractmethod
from typing import Any

from .absStep import AbsStep
from .stepResult import StepResult


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
