from abc import ABC, abstractmethod

from .twitchBanRequest import TwitchBanRequest
from .twitchBanResponse import TwitchBanResponse
from .twitchBannedUserRequest import TwitchBannedUserRequest
from .twitchBannedUsersResponse import TwitchBannedUsersResponse
from .twitchBroadcasterSubscriptionResponse import TwitchBroadcasterSubscriptionResponse
from .twitchEmotesResponse import TwitchEmotesResponse
from .twitchEventSubRequest import TwitchEventSubRequest
from .twitchEventSubResponse import TwitchEventSubResponse
from .twitchFollower import TwitchFollower
from .twitchLiveUserDetails import TwitchLiveUserDetails
from .twitchModUser import TwitchModUser
from .twitchSendChatMessageRequest import TwitchSendChatMessageRequest
from .twitchSendChatMessageResponse import TwitchSendChatMessageResponse
from .twitchTokensDetails import TwitchTokensDetails
from .twitchUnbanRequest import TwitchUnbanRequest
from .twitchUserDetails import TwitchUserDetails
from .twitchUserSubscriptionDetails import TwitchUserSubscriptionDetails
from .twitchValidationResponse import TwitchValidationResponse


class TwitchApiServiceInterface(ABC):

    @abstractmethod
    async def addModerator(
        self,
        broadcasterId: str,
        twitchAccessToken: str,
        userId: str
    ) -> bool:
        pass

    @abstractmethod
    async def banUser(
        self,
        twitchAccessToken: str,
        banRequest: TwitchBanRequest
    ) -> TwitchBanResponse:
        pass

    @abstractmethod
    async def createEventSubSubscription(
        self,
        twitchAccessToken: str,
        eventSubRequest: TwitchEventSubRequest
    ) -> TwitchEventSubResponse:
        pass

    @abstractmethod
    async def fetchBannedUsers(
        self,
        twitchAccessToken: str,
        bannedUserRequest: TwitchBannedUserRequest
    ) -> TwitchBannedUsersResponse:
        pass

    @abstractmethod
    async def fetchBroadcasterSubscription(
        self,
        broadcasterId: str,
        chatterUserId: str,
        twitchAccessToken: str
    ) -> TwitchBroadcasterSubscriptionResponse:
        pass

    @abstractmethod
    async def fetchEmotes(
        self,
        broadcasterId: str,
        twitchAccessToken: str
    ) -> TwitchEmotesResponse:
        pass

    @abstractmethod
    async def fetchFollower(
        self,
        broadcasterId: str,
        twitchAccessToken: str,
        userId: str
    ) -> TwitchFollower | None:
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
        userId: str
    ) -> TwitchModUser | None:
        pass

    @abstractmethod
    async def fetchTokens(self, code: str) -> TwitchTokensDetails:
        pass

    @abstractmethod
    async def fetchUserDetailsWithUserId(
        self,
        twitchAccessToken: str,
        userId: str
    ) -> TwitchUserDetails | None:
        pass

    @abstractmethod
    async def fetchUserDetailsWithUserName(
        self,
        twitchAccessToken: str,
        userName: str
    ) -> TwitchUserDetails | None:
        pass

    @abstractmethod
    async def fetchUserSubscriptionDetails(
        self,
        broadcasterId: str,
        twitchAccessToken: str,
        userId: str
    ) -> TwitchUserSubscriptionDetails | None:
        pass

    @abstractmethod
    async def refreshTokens(self, twitchRefreshToken: str) -> TwitchTokensDetails:
        pass

    @abstractmethod
    async def sendChatMessage(
        self,
        twitchAccessToken: str,
        chatRequest: TwitchSendChatMessageRequest
    ) -> TwitchSendChatMessageResponse:
        pass

    @abstractmethod
    async def unbanUser(
        self,
        twitchAccessToken: str,
        unbanRequest: TwitchUnbanRequest
    ) -> bool:
        pass

    @abstractmethod
    async def validate(self, twitchAccessToken: str) -> TwitchValidationResponse:
        pass
