from abc import ABC, abstractmethod

from .twitchConfigurationType import TwitchConfigurationType


class TwitchAuthor(ABC):

    @abstractmethod
    def getDisplayName(self) -> str:
        pass

    @abstractmethod
    def getId(self) -> str:
        pass

    @abstractmethod
    def getName(self) -> str:
        pass

    @abstractmethod
    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        pass

    @abstractmethod
    def isMod(self) -> bool:
        pass

    @abstractmethod
    def isVip(self) -> bool:
        pass
