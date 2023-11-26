from abc import ABC, abstractmethod

from soundPlayerHelper.soundAlert import SoundAlert


class SoundPlayerHelperInterface(ABC):

    @abstractmethod
    async def play(self, soundAlert: SoundAlert):
        pass
