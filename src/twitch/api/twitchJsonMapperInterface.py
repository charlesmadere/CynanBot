from abc import ABC, abstractmethod
from typing import Any

from .twitchApiScope import TwitchApiScope
from .twitchBanRequest import TwitchBanRequest
from .twitchBroadcasterType import TwitchBroadcasterType
from .twitchEmoteDetails import TwitchEmoteDetails
from .twitchEmoteImageFormat import TwitchEmoteImageFormat
from .twitchEmoteImageScale import TwitchEmoteImageScale
from .twitchEmotesResponse import TwitchEmotesResponse
from .twitchEmoteType import TwitchEmoteType
from .twitchSendChatDropReason import TwitchSendChatDropReason
from .twitchSendChatMessageResponse import TwitchSendChatMessageResponse
from .twitchSubscriberTier import TwitchSubscriberTier
from .twitchThemeMode import TwitchThemeMode
from .twitchTokensDetails import TwitchTokensDetails
from .twitchValidationResponse import TwitchValidationResponse


class TwitchJsonMapperInterface(ABC):

    @abstractmethod
    async def parseApiScope(
        self,
        apiScope: str | None
    ) -> TwitchApiScope | None:
        pass

    @abstractmethod
    async def parseBroadcasterType(
        self,
        broadcasterType: str | None
    ) -> TwitchBroadcasterType | None:
        pass

    @abstractmethod
    async def parseEmoteDetails(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchEmoteDetails | None:
        pass

    @abstractmethod
    async def parseEmoteImageFormat(
        self,
        emoteImageFormat: str | None
    ) -> TwitchEmoteImageFormat | None:
        pass

    @abstractmethod
    async def parseEmoteImageScale(
        self,
        emoteImageScale: str | None
    ) -> TwitchEmoteImageScale | None:
        pass

    @abstractmethod
    async def parseEmotesResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchEmotesResponse | None:
        pass

    @abstractmethod
    async def parseEmoteType(
        self,
        emoteType: str | None
    ) -> TwitchEmoteType | None:
        pass

    @abstractmethod
    async def parseSendChatDropReason(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchSendChatDropReason | None:
        pass

    @abstractmethod
    async def parseSendChatMessageResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchSendChatMessageResponse | None:
        pass

    @abstractmethod
    async def parseSubscriberTier(
        self,
        subscriberTier: str | None
    ) -> TwitchSubscriberTier | None:
        pass

    @abstractmethod
    async def parseThemeMode(
        self,
        themeMode: str | None
    ) -> TwitchThemeMode | None:
        pass

    @abstractmethod
    async def parseTokensDetails(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchTokensDetails | None:
        pass

    @abstractmethod
    async def parseValidationResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchValidationResponse | None:
        pass

    @abstractmethod
    async def requireSubscriberTier(
        self,
        subscriberTier: str | None
    ) -> TwitchSubscriberTier:
        pass

    @abstractmethod
    async def serializeBanRequest(
        self,
        banRequest: TwitchBanRequest
    ) -> dict[str, Any]:
        pass
