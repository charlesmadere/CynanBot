from typing import Final

from frozendict import frozendict

from .anivUserIdsRepositoryInterface import AnivUserIdsRepositoryInterface
from ..models.whichAnivUser import WhichAnivUser
from ...misc import utils as utils
from ...twitch.friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface


class AnivUserIdsRepository(AnivUserIdsRepositoryInterface):

    def __init__(
        self,
        twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface,
    ):
        if not isinstance(twitchFriendsUserIdRepository, TwitchFriendsUserIdRepositoryInterface):
            raise TypeError(f'twitchFriendsUserIdRepository argument is malformed: \"{twitchFriendsUserIdRepository}\"')

        self.__twitchFriendsUserIdRepository: Final[TwitchFriendsUserIdRepositoryInterface] = twitchFriendsUserIdRepository

    async def determineAnivUser(
        self,
        chatterUserId: str | None,
    ) -> WhichAnivUser | None:
        if not utils.isValidStr(chatterUserId):
            return None

        allAnivUsers = await self.getAllUsers()
        allAnivUserIds = frozenset(allAnivUsers.values())

        if chatterUserId not in allAnivUserIds:
            return None

        for anivUser, anivUserId in allAnivUsers.items():
            if anivUserId == chatterUserId:
                return anivUser

        return None

    async def getAcacUserId(self) -> str | None:
        return await self.__twitchFriendsUserIdRepository.getAcacUserId()

    async def getAlbeeevUserId(self) -> str | None:
        return await self.__twitchFriendsUserIdRepository.getAlbeeevUserId()

    async def getAllUsers(self) -> frozendict[WhichAnivUser, str | None]:
        acacUserId = await self.getAcacUserId()
        albeeevUserId = await self.getAlbeeevUserId()
        aneevUserId = await self.getAneevUserId()
        anivUserId = await self.getAnivUserId()

        return frozendict({
            WhichAnivUser.ACAC: acacUserId,
            WhichAnivUser.ALBEEEV: albeeevUserId,
            WhichAnivUser.ANEEV: aneevUserId,
            WhichAnivUser.ANIV: anivUserId,
        })

    async def getAnivUserId(self) -> str | None:
        return await self.__twitchFriendsUserIdRepository.getAnivUserId()

    async def getAneevUserId(self) -> str | None:
        return await self.__twitchFriendsUserIdRepository.getAneevUserId()
