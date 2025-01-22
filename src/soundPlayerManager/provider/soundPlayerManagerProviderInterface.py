from abc import ABC, abstractmethod

from ..soundPlayerManagerInterface import SoundPlayerManagerInterface


class SoundPlayerManagerProviderInterface(ABC):

    @abstractmethod
    def constructNewSoundPlayerManagerInstance(self) -> SoundPlayerManagerInterface:
        pass

    @abstractmethod
    def getSharedSoundPlayerManagerInstance(self) -> SoundPlayerManagerInterface:
        pass
