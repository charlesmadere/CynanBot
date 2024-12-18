from abc import ABC, abstractmethod

from .soundAlert import SoundAlert


class SoundAlertJsonMapperInterface(ABC):

    @abstractmethod
    def parseSoundAlert(
        self,
        jsonString: str | None
    ) -> SoundAlert | None:
        pass

    @abstractmethod
    def serializeSoundAlert(
        self,
        soundAlert: SoundAlert
    ) -> str:
        pass
