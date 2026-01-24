from abc import ABC, abstractmethod
from typing import Any

from ..models.twitchApiScope import TwitchApiScope
from ..models.twitchBanRequest import TwitchBanRequest
from ..models.twitchBanResponse import TwitchBanResponse
from ..models.twitchBanResponseEntry import TwitchBanResponseEntry
from ..models.twitchBannedUser import TwitchBannedUser
from ..models.twitchBannedUsersReponse import TwitchBannedUsersResponse
from ..models.twitchBroadcasterSubscription import TwitchBroadcasterSubscription
from ..models.twitchBroadcasterSubscriptionsResponse import TwitchBroadcasterSubscriptionsResponse
from ..models.twitchBroadcasterType import TwitchBroadcasterType
from ..models.twitchChannelEditor import TwitchChannelEditor
from ..models.twitchChannelEditorsResponse import TwitchChannelEditorsResponse
from ..models.twitchChannelPointsVoting import TwitchChannelPointsVoting
from ..models.twitchChatAnnouncementColor import TwitchChatAnnouncementColor
from ..models.twitchChatBadge import TwitchChatBadge
from ..models.twitchChatMessage import TwitchChatMessage
from ..models.twitchChatMessageFragment import TwitchChatMessageFragment
from ..models.twitchChatMessageFragmentCheermote import TwitchChatMessageFragmentCheermote
from ..models.twitchChatMessageFragmentEmote import TwitchChatMessageFragmentEmote
from ..models.twitchChatMessageFragmentMention import TwitchChatMessageFragmentMention
from ..models.twitchChatMessageFragmentType import TwitchChatMessageFragmentType
from ..models.twitchChatMessageType import TwitchChatMessageType
from ..models.twitchChatter import TwitchChatter
from ..models.twitchChattersResponse import TwitchChattersResponse
from ..models.twitchCheerMetadata import TwitchCheerMetadata
from ..models.twitchCommunitySubGift import TwitchCommunitySubGift
from ..models.twitchConduitRequest import TwitchConduitRequest
from ..models.twitchConduitResponse import TwitchConduitResponse
from ..models.twitchConduitResponseEntry import TwitchConduitResponseEntry
from ..models.twitchConduitShard import TwitchConduitShard
from ..models.twitchContribution import TwitchContribution
from ..models.twitchContributionType import TwitchContributionType
from ..models.twitchEmoteDetails import TwitchEmoteDetails
from ..models.twitchEmoteImageFormat import TwitchEmoteImageFormat
from ..models.twitchEmoteImageScale import TwitchEmoteImageScale
from ..models.twitchEmoteType import TwitchEmoteType
from ..models.twitchEmotesResponse import TwitchEmotesResponse
from ..models.twitchEventSubDetails import TwitchEventSubDetails
from ..models.twitchEventSubRequest import TwitchEventSubRequest
from ..models.twitchEventSubResponse import TwitchEventSubResponse
from ..models.twitchFollower import TwitchFollower
from ..models.twitchFollowersResponse import TwitchFollowersResponse
from ..models.twitchHypeTrainType import TwitchHypeTrainType
from ..models.twitchModeratorUser import TwitchModeratorUser
from ..models.twitchModeratorsResponse import TwitchModeratorsResponse
from ..models.twitchNoticeType import TwitchNoticeType
from ..models.twitchOutcome import TwitchOutcome
from ..models.twitchOutcomeColor import TwitchOutcomeColor
from ..models.twitchOutcomePredictor import TwitchOutcomePredictor
from ..models.twitchPaginationResponse import TwitchPaginationResponse
from ..models.twitchPollChoice import TwitchPollChoice
from ..models.twitchPollStatus import TwitchPollStatus
from ..models.twitchPowerUp import TwitchPowerUp
from ..models.twitchPowerUpEmote import TwitchPowerUpEmote
from ..models.twitchPowerUpType import TwitchPowerUpType
from ..models.twitchPredictionStatus import TwitchPredictionStatus
from ..models.twitchRaid import TwitchRaid
from ..models.twitchResub import TwitchResub
from ..models.twitchResubscriptionMessage import TwitchResubscriptionMessage
from ..models.twitchResubscriptionMessageEmote import TwitchResubscriptionMessageEmote
from ..models.twitchReward import TwitchReward
from ..models.twitchRewardRedemptionStatus import TwitchRewardRedemptionStatus
from ..models.twitchSendChatAnnouncementRequest import TwitchSendChatAnnouncementRequest
from ..models.twitchSendChatDropReason import TwitchSendChatDropReason
from ..models.twitchSendChatMessageRequest import TwitchSendChatMessageRequest
from ..models.twitchSendChatMessageResponse import TwitchSendChatMessageResponse
from ..models.twitchSendChatMessageResponseEntry import TwitchSendChatMessageResponseEntry
from ..models.twitchStartCommercialDetails import TwitchStartCommercialDetails
from ..models.twitchStartCommercialResponse import TwitchStartCommercialResponse
from ..models.twitchStream import TwitchStream
from ..models.twitchStreamType import TwitchStreamType
from ..models.twitchStreamsResponse import TwitchStreamsResponse
from ..models.twitchSub import TwitchSub
from ..models.twitchSubGift import TwitchSubGift
from ..models.twitchSubscriberTier import TwitchSubscriberTier
from ..models.twitchThemeMode import TwitchThemeMode
from ..models.twitchTokensDetails import TwitchTokensDetails
from ..models.twitchUser import TwitchUser
from ..models.twitchUserSubscription import TwitchUserSubscription
from ..models.twitchUserSubscriptionsResponse import TwitchUserSubscriptionsResponse
from ..models.twitchUserType import TwitchUserType
from ..models.twitchUsersResponse import TwitchUsersResponse
from ..models.twitchValidationResponse import TwitchValidationResponse
from ..models.twitchWebsocketCondition import TwitchWebsocketCondition
from ..models.twitchWebsocketConnectionStatus import TwitchWebsocketConnectionStatus
from ..models.twitchWebsocketMessageType import TwitchWebsocketMessageType
from ..models.twitchWebsocketMetadata import TwitchWebsocketMetadata
from ..models.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from ..models.twitchWebsocketTransport import TwitchWebsocketTransport
from ..models.twitchWebsocketTransportMethod import TwitchWebsocketTransportMethod


class TwitchJsonMapperInterface(ABC):

    @abstractmethod
    async def mergeEventSubResponses(
        self,
        first: TwitchEventSubResponse | None,
        second: TwitchEventSubResponse | None,
    ) -> TwitchEventSubResponse | None:
        pass

    @abstractmethod
    async def parseApiScope(
        self,
        apiScope: str | Any | None
    ) -> TwitchApiScope | None:
        pass

    @abstractmethod
    async def parseBanResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchBanResponse | None:
        pass

    @abstractmethod
    async def parseBanResponseEntry(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchBanResponseEntry:
        pass

    @abstractmethod
    async def parseBannedUser(
        self,
        jsonResponse: dict[str, Any] | Any | None,
    ) -> TwitchBannedUser | None:
        pass

    @abstractmethod
    async def parseBannedUsersResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None,
    ) -> TwitchBannedUsersResponse | None:
        pass

    @abstractmethod
    async def parseBroadcasterSubscription(
        self,
        jsonResponse: dict[str, Any] | Any | None,
    ) -> TwitchBroadcasterSubscription | None:
        pass

    @abstractmethod
    async def parseBroadcasterSubscriptionsResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None,
    ) -> TwitchBroadcasterSubscriptionsResponse | None:
        pass

    @abstractmethod
    async def parseBroadcasterType(
        self,
        broadcasterType: str | Any | None,
    ) -> TwitchBroadcasterType:
        pass

    @abstractmethod
    async def parseChannelEditor(
        self,
        jsonResponse: dict[str, Any] | Any | None,
    ) -> TwitchChannelEditor | None:
        pass

    @abstractmethod
    async def parseChannelEditorsResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None,
    ) -> TwitchChannelEditorsResponse | None:
        pass

    @abstractmethod
    async def parseChannelPointsVoting(
        self,
        jsonResponse: dict[str, Any] | Any | None,
    ) -> TwitchChannelPointsVoting | None:
        pass

    @abstractmethod
    async def parseChatBadge(
        self,
        jsonResponse: dict[str, Any] | Any | None,
    ) -> TwitchChatBadge | None:
        pass

    @abstractmethod
    async def parseChatMessage(
        self,
        jsonResponse: dict[str, Any] | Any | None,
    ) -> TwitchChatMessage | None:
        pass

    @abstractmethod
    async def parseChatMessageFragment(
        self,
        jsonResponse: dict[str, Any] | Any | None,
    ) -> TwitchChatMessageFragment | None:
        pass

    @abstractmethod
    async def parseChatMessageFragmentCheermote(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchChatMessageFragmentCheermote | None:
        pass

    @abstractmethod
    async def parseChatMessageFragmentEmote(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchChatMessageFragmentEmote | None:
        pass

    @abstractmethod
    async def parseChatMessageFragmentMention(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchChatMessageFragmentMention | None:
        pass

    @abstractmethod
    async def parseChatMessageFragmentType(
        self,
        fragmentType: str | Any | None
    ) -> TwitchChatMessageFragmentType | None:
        pass

    @abstractmethod
    async def parseChatMessageType(
        self,
        messageType: str | Any | None
    ) -> TwitchChatMessageType | None:
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
        jsonResponse: dict[str, Any] | Any | None,
    ) -> TwitchChattersResponse | None:
        pass

    @abstractmethod
    async def parseCheerMetadata(
        self,
        jsonResponse: dict[str, Any] | Any | None,
    ) -> TwitchCheerMetadata | None:
        pass

    @abstractmethod
    async def parseCommunitySubGift(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchCommunitySubGift | None:
        pass

    @abstractmethod
    async def parseConduitResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None,
    ) -> TwitchConduitResponse | None:
        pass

    @abstractmethod
    async def parseConduitResponseEntry(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchConduitResponseEntry | None:
        pass

    @abstractmethod
    async def parseConduitShard(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchConduitShard | None:
        pass

    @abstractmethod
    async def parseConnectionStatus(
        self,
        connectionStatus: str | Any | None
    ) -> TwitchWebsocketConnectionStatus | None:
        pass

    @abstractmethod
    async def parseContribution(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchContribution | None:
        pass

    @abstractmethod
    async def parseContributionType(
        self,
        contributionType: str | Any | None
    ) -> TwitchContributionType | None:
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
        emoteImageFormat: str | Any | None
    ) -> TwitchEmoteImageFormat | None:
        pass

    @abstractmethod
    async def parseEmoteImageScale(
        self,
        emoteImageScale: str | Any | None
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
        emoteType: str | Any | None
    ) -> TwitchEmoteType | None:
        pass

    @abstractmethod
    async def parseEventSubDetails(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchEventSubDetails | None:
        pass

    @abstractmethod
    async def parseEventSubResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None,
    ) -> TwitchEventSubResponse | None:
        pass

    @abstractmethod
    async def parseFollower(
        self,
        jsonResponse: dict[str, Any] | Any | None,
    ) -> TwitchFollower | None:
        pass

    @abstractmethod
    async def parseFollowersResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None,
    ) -> TwitchFollowersResponse | None:
        pass

    @abstractmethod
    async def parseHypeTrainType(
        self,
        hypeTrainType: str | Any | None,
    ) -> TwitchHypeTrainType | None:
        pass

    @abstractmethod
    async def parseModeratorsResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None,
    ) -> TwitchModeratorsResponse | None:
        pass

    @abstractmethod
    async def parseModeratorUser(
        self,
        jsonResponse: dict[str, Any] | Any | None,
    ) -> TwitchModeratorUser | None:
        pass

    @abstractmethod
    async def parseNoticeType(
        self,
        noticeType: str | Any | None,
    ) -> TwitchNoticeType | None:
        pass

    @abstractmethod
    async def parseOutcome(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchOutcome | None:
        pass

    @abstractmethod
    async def parseOutcomeColor(
        self,
        outcomeColor: str | Any | None
    ) -> TwitchOutcomeColor | None:
        pass

    @abstractmethod
    async def parseOutcomePredictor(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchOutcomePredictor | None:
        pass

    @abstractmethod
    async def parsePaginationResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None,
    ) -> TwitchPaginationResponse | None:
        pass

    @abstractmethod
    async def parsePollChoice(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchPollChoice | None:
        pass

    @abstractmethod
    async def parsePollStatus(
        self,
        pollStatus: str | Any | None
    ) -> TwitchPollStatus | None:
        pass

    @abstractmethod
    async def parsePowerUp(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchPowerUp | None:
        pass

    @abstractmethod
    async def parsePowerUpEmote(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchPowerUpEmote | None:
        pass

    @abstractmethod
    async def parsePowerUpType(
        self,
        powerUpType: str | Any | None
    ) -> TwitchPowerUpType | None:
        pass

    @abstractmethod
    async def parsePredictionStatus(
        self,
        predictionStatus: str | Any | None
    ) -> TwitchPredictionStatus | None:
        pass

    @abstractmethod
    async def parseRaid(
        self,
        jsonResponse: dict[str, Any] | Any | None,
    ) -> TwitchRaid | None:
        pass

    @abstractmethod
    async def parseResub(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchResub | None:
        pass

    @abstractmethod
    async def parseResubscriptionMessage(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchResubscriptionMessage | None:
        pass

    @abstractmethod
    async def parseResubscriptionMessageEmote(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchResubscriptionMessageEmote | None:
        pass

    @abstractmethod
    async def parseReward(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchReward | None:
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
        jsonResponse: dict[str, Any] | Any | None,
    ) -> TwitchSendChatMessageResponse | None:
        pass

    @abstractmethod
    async def parseSendChatMessageResponseEntry(
        self,
        jsonResponse: dict[str, Any] | Any | None,
    ) -> TwitchSendChatMessageResponseEntry | None:
        pass

    @abstractmethod
    async def parseStartCommercialDetails(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchStartCommercialDetails | None:
        pass

    @abstractmethod
    async def parseStartCommercialResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None,
    ) -> TwitchStartCommercialResponse | None:
        pass

    @abstractmethod
    async def parseStream(
        self,
        jsonResponse: dict[str, Any] | Any | None,
    ) -> TwitchStream | None:
        pass

    @abstractmethod
    async def parseStreamsResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None,
    ) -> TwitchStreamsResponse | None:
        pass

    @abstractmethod
    async def parseStreamType(
        self,
        streamType: str | Any | None,
    ) -> TwitchStreamType:
        pass

    @abstractmethod
    async def parseSub(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchSub | None:
        pass

    @abstractmethod
    async def parseSubGift(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchSubGift | None:
        pass

    @abstractmethod
    async def parseSubscriberTier(
        self,
        subscriberTier: str | Any | None,
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
        themeMode: str | Any | None,
    ) -> TwitchThemeMode | None:
        pass

    @abstractmethod
    async def parseTokensDetails(
        self,
        jsonResponse: dict[str, Any] | Any | None,
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
        transportMethod: str | Any | None,
    ) -> TwitchWebsocketTransportMethod | None:
        pass

    @abstractmethod
    async def parseUser(
        self,
        jsonResponse: dict[str, Any] | Any | None,
    ) -> TwitchUser | None:
        pass

    @abstractmethod
    async def parseUsersResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None,
    ) -> TwitchUsersResponse | None:
        pass

    @abstractmethod
    async def parseUserSubscription(
        self,
        jsonResponse: dict[str, Any] | Any | None,
    ) -> TwitchUserSubscription | None:
        pass

    @abstractmethod
    async def parseUserSubscriptionsResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None,
    ) -> TwitchUserSubscriptionsResponse | None:
        pass

    @abstractmethod
    async def parseUserType(
        self,
        userType: str | Any | None,
    ) -> TwitchUserType:
        pass

    @abstractmethod
    async def parseValidationResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchValidationResponse | None:
        pass

    @abstractmethod
    async def parseWebsocketCondition(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchWebsocketCondition | None:
        pass

    @abstractmethod
    async def parseWebsocketMessageType(
        self,
        messageType: str | Any | None
    ) -> TwitchWebsocketMessageType | None:
        pass

    @abstractmethod
    async def parseWebsocketMetadata(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchWebsocketMetadata | None:
        pass

    @abstractmethod
    async def requireChatMessageFragmentType(
        self,
        fragmentType: str | Any | None,
    ) -> TwitchChatMessageFragmentType:
        pass

    @abstractmethod
    async def requireConnectionStatus(
        self,
        connectionStatus: str | Any | None
    ) -> TwitchWebsocketConnectionStatus:
        pass

    @abstractmethod
    async def requireContributionType(
        self,
        contributionType: str | Any | None
    ) -> TwitchContributionType:
        pass

    @abstractmethod
    async def requireNoticeType(
        self,
        noticeType: str | Any | None
    ) -> TwitchNoticeType:
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
        subscriberTier: str | Any | None,
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
    async def requireWebsocketCondition(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchWebsocketCondition:
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
        announcementColor: TwitchChatAnnouncementColor,
    ) -> str:
        pass

    @abstractmethod
    async def serializeCondition(
        self,
        condition: TwitchWebsocketCondition
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    async def serializeConduitRequest(
        self,
        conduitRequest: TwitchConduitRequest
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    async def serializeEventSubRequest(
        self,
        eventSubRequest: TwitchEventSubRequest,
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    async def serializeSendChatAnnouncementRequest(
        self,
        announcementRequest: TwitchSendChatAnnouncementRequest,
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    async def serializeSendChatMessageRequest(
        self,
        chatRequest: TwitchSendChatMessageRequest,
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    async def serializeSubscriberTier(
        self,
        subscriberTier: TwitchSubscriberTier,
    ) -> str:
        pass

    @abstractmethod
    async def serializeSubscriptionType(
        self,
        subscriptionType: TwitchWebsocketSubscriptionType,
    ) -> str:
        pass

    @abstractmethod
    async def serializeTransport(
        self,
        transport: TwitchWebsocketTransport,
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    async def serializeTransportMethod(
        self,
        transportMethod: TwitchWebsocketTransportMethod,
    ) -> str:
        pass

    @abstractmethod
    async def serializeWebsocketConnectionStatus(
        self,
        connectionStatus: TwitchWebsocketConnectionStatus,
    ) -> str:
        pass
