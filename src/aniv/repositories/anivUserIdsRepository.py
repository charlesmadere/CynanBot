from typing import Final

from frozendict import frozendict

from .anivUserIdsRepositoryInterface import AnivUserIdsRepositoryInterface
from ..models.whichAnivUser import WhichAnivUser
from ...twitch.friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface


class AnivUserIdsRepository(AnivUserIdsRepositoryInterface):

    def __init__(
        self,
        twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface,
    ):
        if not isinstance(twitchFriendsUserIdRepository, TwitchFriendsUserIdRepositoryInterface):
            raise TypeError(f'twitchFriendsUserIdRepository argument is malformed: \"{twitchFriendsUserIdRepository}\"')

        self.__twitchFriendsUserIdRepository: Final[TwitchFriendsUserIdRepositoryInterface] = twitchFriendsUserIdRepository

    async def getAcacUserId(self) -> str | None:
        return await self.__twitchFriendsUserIdRepository.getAcacUserId()

    async def getAllUserIds(self) -> frozendict[WhichAnivUser, str | None]:
        acacUserId = await self.getAcacUserId()
        aneevUserId = await self.getAneevUserId()
        anivUserId = await self.getAnivUserId()

        return frozendict({
            WhichAnivUser.ACAC: acacUserId,
            WhichAnivUser.ANEEV: aneevUserId,
            WhichAnivUser.ANIV: anivUserId,
        })

    async def getAnivUserId(self) -> str | None:
        return await self.__twitchFriendsUserIdRepository.getAnivUserId()

    async def getAneevUserId(self) -> str | None:
        return await self.__twitchFriendsUserIdRepository.getAneevUserId()
