from abc import ABC, abstractmethod


class TwitchConstantsInterface(ABC):

    @property
    @abstractmethod
    def maxMessageSize(self) -> int:
        pass

    @property
    @abstractmethod
    def maxTimeoutSeconds(self) -> int:
        pass
