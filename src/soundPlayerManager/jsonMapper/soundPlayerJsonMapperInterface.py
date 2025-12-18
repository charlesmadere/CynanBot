from abc import ABC, abstractmethod
from typing import Any

from ..soundPlayerType import SoundPlayerType


class SoundPlayerJsonMapperInterface(ABC):

    @abstractmethod
    def parseSoundPlayerType(
        self,
        soundPlayerType: str | Any | None,
    ) -> SoundPlayerType:
        pass
