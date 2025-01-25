from abc import ABC, abstractmethod
from typing import Any

from .twitchIrcTags import TwitchIrcTags


class TwitchIrcTagsParserInterface(ABC):

    @abstractmethod
    async def parseTwitchIrcTags(
        self,
        rawIrcTags: dict[Any, Any]
    ) -> TwitchIrcTags:
        pass
