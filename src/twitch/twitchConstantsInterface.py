from abc import ABC, abstractmethod


class TwitchConstantsInterface(ABC):

    @abstractmethod
    def getMaxMessageSize(self) -> int:
        pass

    @abstractmethod
    def getMaxTimeoutSeconds(self) -> int:
        pass
