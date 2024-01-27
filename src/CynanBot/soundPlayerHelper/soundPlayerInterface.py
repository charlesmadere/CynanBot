from abc import ABC, abstractmethod

from CynanBot.soundPlayerHelper.soundReferenceInterface import SoundReferenceInterface

class SoundPlayerInterface(ABC):

    @abstractmethod
    async def load(self, filePath: str) -> SoundReferenceInterface:
        pass
