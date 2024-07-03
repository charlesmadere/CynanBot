from abc import ABC, abstractmethod

from .soundPlayerManagerInterface import SoundPlayerManagerInterface


class SoundPlayerManagerProviderInterface(ABC):

    @abstractmethod
    def constructSoundPlayerManagerInstance(self) -> SoundPlayerManagerInterface:
        pass
