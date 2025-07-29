from abc import ABC, abstractmethod


class AbsTimeoutEvent(ABC):

    @abstractmethod
    def getActionId(self) -> str:
        pass
