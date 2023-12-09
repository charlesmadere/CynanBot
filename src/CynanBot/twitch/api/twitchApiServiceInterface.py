from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from CynanBot.twitch.twitchBannedUserRequest import TwitchBannedUserRequest
from CynanBot.twitch.twitchBannedUsersResponse import TwitchBannedUsersResponse
from CynanBot.twitch.twitchBanRequest import TwitchBanRequest
from CynanBot.twitch.twitchBanResponse import TwitchBanResponse
from CynanBot.twitch.twitchEmoteDetails import TwitchEmoteDetails
from CynanBot.twitch.twitchEventSubRequest import TwitchEventSubRequest
from CynanBot.twitch.twitchEventSubResponse import TwitchEventSubResponse
from CynanBot.twitch.twitchLiveUserDetails import TwitchLiveUserDetails
from CynanBot.twitch.twitchModUser import TwitchModUser
from CynanBot.twitch.twitchTokensDetails import TwitchTokensDetails
from CynanBot.twitch.twitchUnbanRequest import TwitchUnbanRequest
from CynanBot.twitch.twitchUserDetails import TwitchUserDetails
from CynanBot.twitch.twitchUserSubscriptionDetails import \
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
    ) -> List[TwitchEmoteDetails]:
        pass

    @abstractmethod
    async def fetchLiveUserDetails(
        self,
        twitchAccessToken: str,
        userNames: List[str]
    ) -> List[TwitchLiveUserDetails]:
        pass

    @abstractmethod
    async def fetchModerator(
        self,
        broadcasterId: str,
        twitchAccessToken: str,
        userId: str
    ) -> Optional[TwitchModUser]:
        pass

    @abstractmethod
    async def fetchTokens(self, code: str) -> TwitchTokensDetails:
        pass

    @abstractmethod
    async def fetchUserDetailsWithUserId(
        self,
        twitchAccessToken: str,
        userId: str
    ) -> Optional[TwitchUserDetails]:
        pass

    @abstractmethod
    async def fetchUserDetailsWithUserName(
        self,
        twitchAccessToken: str,
        userName: str
    ) -> Optional[TwitchUserDetails]:
        pass

    @abstractmethod
    async def fetchUserSubscriptionDetails(
        self,
        broadcasterId: str,
        twitchAccessToken: str,
        userId: str
    ) -> Optional[TwitchUserSubscriptionDetails]:
        pass

    @abstractmethod
    async def refreshTokens(self, twitchRefreshToken: str) -> TwitchTokensDetails:
        pass

    @abstractmethod
    async def unbanUser(
        self,
        twitchAccessToken: str,
        unbanRequest: TwitchUnbanRequest
    ) -> bool:
        pass

    @abstractmethod
    async def validateTokens(self, twitchAccessToken: str) -> Optional[datetime]:
        pass
