from abc import ABC, abstractmethod
from typing import Any

from .absStep import AbsStep
from .stepResult import StepResult
from ..cheerActionType import CheerActionType


class AbsSteps(ABC):

    @property
    @abstractmethod
    def cheerActionType(self) -> CheerActionType:
        pass

    @property
    @abstractmethod
    def currentStep(self) -> AbsStep:
        pass

    @abstractmethod
    def stepForward(self) -> StepResult:
        pass

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'cheerActionType': self.cheerActionType,
            'currentStep': self.currentStep,
        }
