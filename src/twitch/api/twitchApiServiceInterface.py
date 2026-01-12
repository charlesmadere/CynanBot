from abc import ABC, abstractmethod

from .models.twitchBanRequest import TwitchBanRequest
from .models.twitchBanResponse import TwitchBanResponse
from .models.twitchBannedUsersReponse import TwitchBannedUsersResponse
from .models.twitchBroadcasterSubscriptionsResponse import TwitchBroadcasterSubscriptionsResponse
from .models.twitchChannelEditorsResponse import TwitchChannelEditorsResponse
from .models.twitchChattersRequest import TwitchChattersRequest
from .models.twitchChattersResponse import TwitchChattersResponse
from .models.twitchEmotesResponse import TwitchEmotesResponse
from .models.twitchEventSubRequest import TwitchEventSubRequest
from .models.twitchEventSubResponse import TwitchEventSubResponse
from .models.twitchFollowersResponse import TwitchFollowersResponse
from .models.twitchLiveUserDetails import TwitchLiveUserDetails
from .models.twitchModeratorsResponse import TwitchModeratorsResponse
from .models.twitchSendChatAnnouncementRequest import TwitchSendChatAnnouncementRequest
from .models.twitchSendChatMessageRequest import TwitchSendChatMessageRequest
from .models.twitchSendChatMessageResponse import TwitchSendChatMessageResponse
from .models.twitchStartCommercialResponse import TwitchStartCommercialResponse
from .models.twitchTokensDetails import TwitchTokensDetails
from .models.twitchUnbanRequest import TwitchUnbanRequest
from .models.twitchUserDetails import TwitchUserDetails
from .models.twitchUserSubscriptionsResponse import TwitchUserSubscriptionsResponse
from .models.twitchValidationResponse import TwitchValidationResponse


class TwitchApiServiceInterface(ABC):

    @abstractmethod
    async def addModerator(
        self,
        broadcasterId: str,
        twitchAccessToken: str,
        userId: str,
    ) -> bool:
        pass

    @abstractmethod
    async def banUser(
        self,
        twitchAccessToken: str,
        banRequest: TwitchBanRequest,
    ) -> TwitchBanResponse:
        pass

    @abstractmethod
    async def checkUserSubscription(
        self,
        broadcasterId: str,
        twitchAccessToken: str,
        userId: str,
    ) -> TwitchUserSubscriptionsResponse:
        pass

    @abstractmethod
    async def createEventSubSubscription(
        self,
        twitchAccessToken: str,
        eventSubRequest: TwitchEventSubRequest,
    ) -> TwitchEventSubResponse:
        pass

    @abstractmethod
    async def fetchBannedUsers(
        self,
        broadcasterId: str,
        twitchAccessToken: str,
        userId: str,
    ) -> TwitchBannedUsersResponse:
        pass

    @abstractmethod
    async def fetchBroadcasterSubscriptions(
        self,
        broadcasterId: str,
        twitchAccessToken: str,
        userId: str,
    ) -> TwitchBroadcasterSubscriptionsResponse:
        pass

    @abstractmethod
    async def fetchChannelEditors(
        self,
        broadcasterId: str,
        twitchAccessToken: str,
    ) -> TwitchChannelEditorsResponse:
        pass

    @abstractmethod
    async def fetchChatters(
        self,
        twitchAccessToken: str,
        chattersRequest: TwitchChattersRequest,
    ) -> TwitchChattersResponse:
        pass

    @abstractmethod
    async def fetchChannelEmotes(
        self,
        broadcasterId: str,
        twitchAccessToken: str,
    ) -> TwitchEmotesResponse:
        pass

    @abstractmethod
    async def fetchEventSubSubscriptions(
        self,
        twitchAccessToken: str,
        userId: str,
    ) -> TwitchEventSubResponse:
        pass

    @abstractmethod
    async def fetchFollower(
        self,
        broadcasterId: str,
        twitchAccessToken: str,
        userId: str,
    ) -> TwitchFollowersResponse | None:
        pass

    @abstractmethod
    async def fetchLiveUserDetails(
        self,
        twitchAccessToken: str,
        twitchChannelIds: list[str]
    ) -> list[TwitchLiveUserDetails]:
        pass

    @abstractmethod
    async def fetchModerator(
        self,
        broadcasterId: str,
        twitchAccessToken: str,
        userId: str,
    ) -> TwitchModeratorsResponse:
        pass

    @abstractmethod
    async def fetchTokens(self, code: str) -> TwitchTokensDetails:
        pass

    @abstractmethod
    async def fetchUserDetailsWithUserId(
        self,
        twitchAccessToken: str,
        userId: str,
    ) -> TwitchUserDetails | None:
        pass

    @abstractmethod
    async def fetchUserDetailsWithUserName(
        self,
        twitchAccessToken: str,
        userName: str,
    ) -> TwitchUserDetails | None:
        pass

    @abstractmethod
    async def refreshTokens(self, twitchRefreshToken: str) -> TwitchTokensDetails:
        pass

    @abstractmethod
    async def removeModerator(
        self,
        broadcasterId: str,
        moderatorId: str,
        twitchAccessToken: str,
    ) -> bool:
        pass

    @abstractmethod
    async def sendChatAnnouncement(
        self,
        twitchAccessToken: str,
        announcementRequest: TwitchSendChatAnnouncementRequest,
    ) -> bool:
        pass

    @abstractmethod
    async def sendChatMessage(
        self,
        twitchAccessToken: str,
        chatRequest: TwitchSendChatMessageRequest,
    ) -> TwitchSendChatMessageResponse:
        pass

    @abstractmethod
    async def startCommercial(
        self,
        length: int,
        broadcasterId: str,
        twitchAccessToken: str,
    ) -> TwitchStartCommercialResponse:
        pass

    @abstractmethod
    async def unbanUser(
        self,
        twitchAccessToken: str,
        unbanRequest: TwitchUnbanRequest,
    ) -> bool:
        pass

    @abstractmethod
    async def validate(self, twitchAccessToken: str) -> TwitchValidationResponse:
        pass
