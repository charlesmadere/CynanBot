from abc import ABC, abstractmethod
from typing import Any

from ..soundAlert import SoundAlert


class SoundAlertJsonMapperInterface(ABC):

    @abstractmethod
    def parseSoundAlert(
        self,
        jsonString: str | Any | None,
    ) -> SoundAlert | None:
        pass

    @abstractmethod
    def requireSoundAlert(
        self,
        jsonString: str | Any | None,
    ) -> SoundAlert:
        pass

    @abstractmethod
    def serializeSoundAlert(
        self,
        soundAlert: SoundAlert,
    ) -> str:
        pass
