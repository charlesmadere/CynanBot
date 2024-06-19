from abc import ABC, abstractmethod

from CynanBot.soundPlayerManager.soundAlert import SoundAlert


class ImmediateStreamAlertsManagerInterface(ABC):

    @abstractmethod
    async def playSoundAlert(self, alert: SoundAlert):
        pass

    @abstractmethod
    async def playSoundFile(self, file: str):
        pass
