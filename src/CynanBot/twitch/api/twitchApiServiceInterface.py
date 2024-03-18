from abc import ABC, abstractmethod
from datetime import datetime

from CynanBot.twitch.api.twitchBannedUserRequest import TwitchBannedUserRequest
from CynanBot.twitch.api.twitchBannedUsersResponse import \
    TwitchBannedUsersResponse
from CynanBot.twitch.api.twitchBanRequest import TwitchBanRequest
from CynanBot.twitch.api.twitchBanResponse import TwitchBanResponse
from CynanBot.twitch.api.twitchEmoteDetails import TwitchEmoteDetails
from CynanBot.twitch.api.twitchEventSubRequest import TwitchEventSubRequest
from CynanBot.twitch.api.twitchEventSubResponse import TwitchEventSubResponse
from CynanBot.twitch.api.twitchFollower import TwitchFollower
from CynanBot.twitch.api.twitchLiveUserDetails import TwitchLiveUserDetails
from CynanBot.twitch.api.twitchModUser import TwitchModUser
from CynanBot.twitch.api.twitchSendChatMessageRequest import \
    TwitchSendChatMessageRequest
from CynanBot.twitch.api.twitchSendChatMessageResponse import \
    TwitchSendChatMessageResponse
from CynanBot.twitch.api.twitchTokensDetails import TwitchTokensDetails
from CynanBot.twitch.api.twitchUnbanRequest import TwitchUnbanRequest
from CynanBot.twitch.api.twitchUserDetails import TwitchUserDetails
from CynanBot.twitch.api.twitchUserSubscriptionDetails import \
    TwitchUserSubscriptionDetails


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
    async def fetchEmoteDetails(
        self,
        broadcasterId: str,
        twitchAccessToken: str
    ) -> list[TwitchEmoteDetails]:
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
        userNames: list[str]
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
    async def validateTokens(self, twitchAccessToken: str) -> datetime | None:
        pass
