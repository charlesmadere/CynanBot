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

    @property
    @abstractmethod
    def isLeadMod(self) -> bool:
        pass

    @property
    @abstractmethod
    def isMod(self) -> bool:
        pass

    @property
    @abstractmethod
    def isVip(self) -> bool:
        pass

    @property
    @abstractmethod
    def twitchConfigurationType(self) -> TwitchConfigurationType:
        pass
