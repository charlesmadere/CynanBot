from abc import ABC, abstractmethod
from typing import Optional


class MutableRecurringAction(ABC):

    @abstractmethod
    def setEnabled(self, enabled: bool):
        pass

    @abstractmethod
    def setMinutesBetween(self, minutesBetween: Optional[int]):
        pass
