from abc import ABC, abstractmethod

from ..soundPlayerManagerInterface import SoundPlayerManagerInterface


class SoundPlayerManagerProviderInterface(ABC):

    @abstractmethod
    def constructNewInstance(self) -> SoundPlayerManagerInterface:
        pass

    @abstractmethod
    def getSharedInstance(self) -> SoundPlayerManagerInterface:
        pass
