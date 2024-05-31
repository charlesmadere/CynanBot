from abc import ABC, abstractmethod
from typing import Any

from CynanBot.twitch.api.twitchApiScope import TwitchApiScope
from CynanBot.twitch.api.twitchValidationResponse import \
    TwitchValidationResponse


class TwitchJsonMapperInterface(ABC):

    @abstractmethod
    async def parseApiScope(
        self,
        apiScope: str | None
    ) -> TwitchApiScope | None:
        pass

    @abstractmethod
    async def parseValidationResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchValidationResponse | None:
        pass
