from typing import Final

from src.users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class FakeUserIdsRepository(UserIdsRepositoryInterface):

    def __init__(self):
        self.__userIdsToUserNames: Final[dict[str, str | None]] = {
            '111111': 'CynanBot',
            '222222': 'Eddie',
            '333333': 'imyt',
            '444444': 'smCharles',
            '555555': 'stashiocat',
        }

    async def clearCaches(self):
        # this method is intentionally empty
        pass

    async def fetchUserId(
        self,
        userName: str,
        twitchAccessToken: str | None = None
    ) -> str | None:
        for cachedUserId, cachedUserName in self.__userIdsToUserNames.items():
            if cachedUserName is None:
                continue
            elif cachedUserName.casefold() == userName.casefold():
                return cachedUserId

        return None

    async def fetchUserIdAsInt(
        self,
        userName: str,
        twitchAccessToken: str | None = None
    ) -> int | None:
        cachedUserId = await self.fetchUserId(
            userName = userName,
            twitchAccessToken = twitchAccessToken
        )

        if cachedUserId is None:
            return None
        else:
            return int(cachedUserId)

    async def fetchUserName(
        self,
        userId: str,
        twitchAccessToken: str | None = None
    ) -> str | None:
        return self.__userIdsToUserNames.get(userId, None)

    async def requireUserId(
        self,
        userName: str,
        twitchAccessToken: str | None = None
    ) -> str:
        cachedUserId = await self.fetchUserId(
            userName = userName,
            twitchAccessToken = twitchAccessToken
        )

        if cachedUserId is None:
            raise RuntimeError()
        else:
            return cachedUserId

    async def requireUserIdAsInt(
        self,
        userName: str,
        twitchAccessToken: str | None = None
    ) -> int:
        cachedUserId = await self.requireUserId(
            userName = userName,
            twitchAccessToken = twitchAccessToken
        )

        return int(cachedUserId)

    async def requireUserName(
        self,
        userId: str,
        twitchAccessToken: str | None = None
    ) -> str:
        cachedUserName = await self.fetchUserName(
            userId = userId,
            twitchAccessToken = twitchAccessToken
        )

        if cachedUserName is None:
            raise RuntimeError()
        else:
            return cachedUserName

    async def setUser(
        self,
        userId: str,
        userName: str
    ):
        self.__userIdsToUserNames[userId] = userName

    async def setUsers(
        self,
        userIdToUserName: dict[str, str]
    ):
        for userId, userName in userIdToUserName.values():
            await self.setUser(
                userId = userId,
                userName = userName
            )
