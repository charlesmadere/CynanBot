from abc import ABC, abstractmethod
from typing import Any

from .absStep import AbsStep
from .stepResult import StepResult
from ..actions.recurringActionType import RecurringActionType


class AbsSteps(ABC):

    @property
    @abstractmethod
    def currentStep(self) -> AbsStep:
        pass

    @property
    @abstractmethod
    def recurringActionType(self) -> RecurringActionType:
        pass

    @abstractmethod
    def stepForward(self) -> StepResult:
        pass

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'currentStep': self.currentStep,
            'recurringActionType': self.recurringActionType,
        }
