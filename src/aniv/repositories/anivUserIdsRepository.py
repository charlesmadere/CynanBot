from typing import Final

from frozendict import frozendict

from .anivUserIdsRepositoryInterface import AnivUserIdsRepositoryInterface
from ..models.whichAnivUser import WhichAnivUser
from ...misc import utils as utils


class AnivUserIdsRepository(AnivUserIdsRepositoryInterface):

    def __init__(
        self,
        acacUserId: str | None = '1274825203',
        albeeevUserId: str | None = '1387490799',
        aneevUserId: str | None = '1284413302',
        anivUserId: str | None = '749050409',
    ):
        if acacUserId is not None and not isinstance(acacUserId, str):
            raise TypeError(f'acacUserId argument is malformed: \"{acacUserId}\"')
        elif albeeevUserId is not None and not isinstance(albeeevUserId, str):
            raise TypeError(f'albeeevUserId argument is malformed: \"{albeeevUserId}\"')
        elif aneevUserId is not None and not isinstance(aneevUserId, str):
            raise TypeError(f'aneevUserId argument is malformed: \"{aneevUserId}\"')
        elif anivUserId is not None and not isinstance(anivUserId, str):
            raise TypeError(f'anivUserId argument is malformed: \"{anivUserId}\"')

        self.__acacUserId: Final[str | None] = acacUserId
        self.__albeeevUserId: Final[str | None] = albeeevUserId
        self.__aneevUserId: Final[str | None] = aneevUserId
        self.__anivUserId: Final[str | None] = anivUserId

        self.__cache: frozendict[WhichAnivUser, str | None] | None = None

    async def clearCaches(self):
        self.__cache = None

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
        return self.__acacUserId

    async def getAlbeeevUserId(self) -> str | None:
        return self.__albeeevUserId

    async def getAllUsers(self) -> frozendict[WhichAnivUser, str | None]:
        cache = self.__cache

        if cache is not None:
            return cache

        allUsers: frozendict[WhichAnivUser, str | None] = frozendict({
            WhichAnivUser.ACAC: await self.getAcacUserId(),
            WhichAnivUser.ALBEEEV: await self.getAlbeeevUserId(),
            WhichAnivUser.ANEEV: await self.getAneevUserId(),
            WhichAnivUser.ANIV: await self.getAnivUserId(),
        })

        self.__cache = allUsers
        return allUsers

    async def getAnivUserId(self) -> str | None:
        return self.__anivUserId

    async def getAneevUserId(self) -> str | None:
        return self.__aneevUserId
