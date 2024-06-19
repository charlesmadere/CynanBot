from abc import ABC, abstractmethod

from CynanBot.soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface


class SoundPlayerManagerProviderInterface(ABC):

    @abstractmethod
    def constructSoundPlayerManagerInstance(self) -> SoundPlayerManagerInterface:
        pass
