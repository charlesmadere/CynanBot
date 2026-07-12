from abc import ABC, abstractmethod


class GlobalTwitchConstantsInterface(ABC):

    @abstractmethod
    def getMaxMessageSize(self) -> int:
        pass

    @abstractmethod
    def getMaxTimeoutSeconds(self) -> int:
        pass
