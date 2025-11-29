from abc import ABC, abstractmethod

from ..compositeTtsManagerInterface import CompositeTtsManagerInterface


class CompositeTtsManagerProviderInterface(ABC):

    @abstractmethod
    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True,
    ) -> CompositeTtsManagerInterface:
        pass

    @abstractmethod
    def getSharedInstance(self) -> CompositeTtsManagerInterface:
        pass
