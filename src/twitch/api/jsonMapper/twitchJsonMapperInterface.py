from abc import ABC, abstractmethod
from typing import Any

from ..models.twitchApiScope import TwitchApiScope
from ..models.twitchBanRequest import TwitchBanRequest
from ..models.twitchBannedUserResponse import TwitchBannedUserResponse
from ..models.twitchBroadcasterSubscriptionResponse import TwitchBroadcasterSubscriptionResponse
from ..models.twitchBroadcasterSusbcription import TwitchBroadcasterSubscription
from ..models.twitchBroadcasterType import TwitchBroadcasterType
from ..models.twitchChannelEditor import TwitchChannelEditor
from ..models.twitchChannelEditorsResponse import TwitchChannelEditorsResponse
from ..models.twitchChatAnnouncementColor import TwitchChatAnnouncementColor
from ..models.twitchChatter import TwitchChatter
from ..models.twitchChattersResponse import TwitchChattersResponse
from ..models.twitchCheerMetadata import TwitchCheerMetadata
from ..models.twitchEmoteDetails import TwitchEmoteDetails
from ..models.twitchEmoteImageFormat import TwitchEmoteImageFormat
from ..models.twitchEmoteImageScale import TwitchEmoteImageScale
from ..models.twitchEmoteType import TwitchEmoteType
from ..models.twitchEmotesResponse import TwitchEmotesResponse
from ..models.twitchEventSubRequest import TwitchEventSubRequest
from ..models.twitchOutcomeColor import TwitchOutcomeColor
from ..models.twitchPaginationResponse import TwitchPaginationResponse
from ..models.twitchPollStatus import TwitchPollStatus
from ..models.twitchPredictionStatus import TwitchPredictionStatus
from ..models.twitchRewardRedemptionStatus import TwitchRewardRedemptionStatus
from ..models.twitchSendChatAnnouncementRequest import TwitchSendChatAnnouncementRequest
from ..models.twitchSendChatDropReason import TwitchSendChatDropReason
from ..models.twitchSendChatMessageRequest import TwitchSendChatMessageRequest
from ..models.twitchSendChatMessageResponse import TwitchSendChatMessageResponse
from ..models.twitchStreamType import TwitchStreamType
from ..models.twitchSubscriberTier import TwitchSubscriberTier
from ..models.twitchThemeMode import TwitchThemeMode
from ..models.twitchTokensDetails import TwitchTokensDetails
from ..models.twitchUserSubscription import TwitchUserSubscription
from ..models.twitchUserType import TwitchUserType
from ..models.twitchValidationResponse import TwitchValidationResponse
from ..models.twitchWebsocketCondition import TwitchWebsocketCondition
from ..models.twitchWebsocketConnectionStatus import TwitchWebsocketConnectionStatus
from ..models.twitchWebsocketMessageType import TwitchWebsocketMessageType
from ..models.twitchWebsocketNoticeType import TwitchWebsocketNoticeType
from ..models.twitchWebsocketSub import TwitchWebsocketSub
from ..models.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from ..models.twitchWebsocketTransport import TwitchWebsocketTransport
from ..models.twitchWebsocketTransportMethod import TwitchWebsocketTransportMethod


class TwitchJsonMapperInterface(ABC):

    @abstractmethod
    async def parseApiScope(
        self,
        apiScope: str | None
    ) -> TwitchApiScope | None:
        pass

    @abstractmethod
    async def parseBannedUserResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchBannedUserResponse | None:
        pass

    @abstractmethod
    async def parseBroadcasterSubscription(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchBroadcasterSubscription | None:
        pass

    @abstractmethod
    async def parseBroadcasterSubscriptionResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchBroadcasterSubscriptionResponse | None:
        pass

    @abstractmethod
    async def parseBroadcasterType(
        self,
        broadcasterType: str | None
    ) -> TwitchBroadcasterType:
        pass

    @abstractmethod
    async def parseChannelEditor(
        self,
        jsonResponse: dict[str, Any]
    ) -> TwitchChannelEditor:
        pass

    @abstractmethod
    async def parseChannelEditorsResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchChannelEditorsResponse | None:
        pass

    @abstractmethod
    async def parseChatter(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchChatter:
        pass

    @abstractmethod
    async def parseChattersResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchChattersResponse | None:
        pass

    @abstractmethod
    async def parseCheerMetadata(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchCheerMetadata | None:
        pass

    @abstractmethod
    async def parseCondition(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchWebsocketCondition | None:
        pass

    @abstractmethod
    async def parseConnectionStatus(
        self,
        connectionStatus: str | Any | None
    ) -> TwitchWebsocketConnectionStatus | None:
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
    async def parseNoticeType(
        self,
        noticeType: str | Any | None
    ) -> TwitchWebsocketNoticeType | None:
        pass

    @abstractmethod
    async def parseOutcomeColor(
        self,
        outcomeColor: str | Any | None
    ) -> TwitchOutcomeColor | None:
        pass

    @abstractmethod
    async def parsePaginationResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchPaginationResponse | None:
        pass

    @abstractmethod
    async def parsePollStatus(
        self,
        pollStatus: str | Any | None
    ) -> TwitchPollStatus | None:
        pass

    @abstractmethod
    async def parsePredictionStatus(
        self,
        predictionStatus: str | Any | None
    ) -> TwitchPredictionStatus | None:
        pass

    @abstractmethod
    async def parseRewardRedemptionStatus(
        self,
        rewardRedemptionStatus: str | Any | None
    ) -> TwitchRewardRedemptionStatus | None:
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
    async def parseStreamType(
        self,
        streamType: str | None
    ) -> TwitchStreamType:
        pass

    @abstractmethod
    async def parseSubscriberTier(
        self,
        subscriberTier: str | None
    ) -> TwitchSubscriberTier | None:
        pass

    @abstractmethod
    async def parseSubscriptionType(
        self,
        subscriptionType: str | Any | None
    ) -> TwitchWebsocketSubscriptionType | None:
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
    async def parseTransport(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchWebsocketTransport | None:
        pass

    @abstractmethod
    async def parseTransportMethod(
        self,
        transportMethod: str | Any | None
    ) -> TwitchWebsocketTransportMethod | None:
        pass

    @abstractmethod
    async def parseUserSubscription(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchUserSubscription | None:
        pass

    @abstractmethod
    async def parseUserType(
        self,
        userType: str | Any | None
    ) -> TwitchUserType:
        pass

    @abstractmethod
    async def parseValidationResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchValidationResponse | None:
        pass

    @abstractmethod
    async def parseWebsocketMessageType(
        self,
        messageType: str | Any | None
    ) -> TwitchWebsocketMessageType | None:
        pass

    @abstractmethod
    async def parseWebsocketSub(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchWebsocketSub | None:
        pass

    @abstractmethod
    async def requireConnectionStatus(
        self,
        connectionStatus: str | Any | None
    ) -> TwitchWebsocketConnectionStatus:
        pass

    @abstractmethod
    async def requireNoticeType(
        self,
        noticeType: str | Any | None
    ) -> TwitchWebsocketNoticeType:
        pass

    @abstractmethod
    async def requireOutcomeColor(
        self,
        outcomeColor: str | Any | None
    ) -> TwitchOutcomeColor:
        pass

    @abstractmethod
    async def requireSubscriberTier(
        self,
        subscriberTier: str | None
    ) -> TwitchSubscriberTier:
        pass

    @abstractmethod
    async def requireSubscriptionType(
        self,
        subscriptionType: str | Any | None
    ) -> TwitchWebsocketSubscriptionType:
        pass

    @abstractmethod
    async def requireTransport(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchWebsocketTransport:
        pass

    @abstractmethod
    async def requireTransportMethod(
        self,
        transportMethod: str | Any | None
    ) -> TwitchWebsocketTransportMethod:
        pass

    @abstractmethod
    async def requireWebsocketMessageType(
        self,
        messageType: str | Any | None
    ) -> TwitchWebsocketMessageType:
        pass

    @abstractmethod
    async def serializeBanRequest(
        self,
        banRequest: TwitchBanRequest
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    async def serializeChatAnnouncementColor(
        self,
        announcementColor: TwitchChatAnnouncementColor
    ) -> str:
        pass

    @abstractmethod
    async def serializeCondition(
        self,
        condition: TwitchWebsocketCondition
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    async def serializeEventSubRequest(
        self,
        eventSubRequest: TwitchEventSubRequest
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    async def serializeSendChatAnnouncementRequest(
        self,
        announcementRequest: TwitchSendChatAnnouncementRequest
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    async def serializeSendChatMessageRequest(
        self,
        chatRequest: TwitchSendChatMessageRequest
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    async def serializeSubscriptionType(
        self,
        subscriptionType: TwitchWebsocketSubscriptionType
    ) -> str:
        pass

    @abstractmethod
    async def serializeTransport(
        self,
        transport: TwitchWebsocketTransport
    ) -> dict[str, Any]:
        pass