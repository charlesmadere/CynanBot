from abc import ABC, abstractmethod
from typing import Optional

from CynanBot.soundPlayerHelper.soundReferenceInterface import \
    SoundReferenceInterface


class SoundPlayerInterface(ABC):

    @abstractmethod
    async def load(self, filePath: Optional[str]) -> SoundReferenceInterface:
        pass
