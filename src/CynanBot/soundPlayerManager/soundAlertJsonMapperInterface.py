from abc import ABC, abstractmethod

from CynanBot.soundPlayerManager.soundAlert import SoundAlert


class SoundAlertJsonMapperInterface(ABC):

    @abstractmethod
    def parseSoundAlert(
        self,
        jsonString: str | None
    ) -> SoundAlert | None:
        pass
