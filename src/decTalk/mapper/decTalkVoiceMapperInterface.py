from abc import ABC, abstractmethod
from typing import Any

from ..models.decTalkVoice import DecTalkVoice


class DecTalkVoiceMapperInterface(ABC):

    @abstractmethod
    async def parseVoice(
        self,
        string: str | Any | None
    ) -> DecTalkVoice | None:
        pass

    @abstractmethod
    async def requireVoice(
        self,
        voice: str | Any | None
    ) -> DecTalkVoice:
        pass

    @abstractmethod
    async def serializeVoice(
        self,
        voice: DecTalkVoice
    ) -> str:
        pass
