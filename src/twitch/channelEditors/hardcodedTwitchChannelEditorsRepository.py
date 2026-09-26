from typing import Collection, Final

from .hardcodedTwitchChannelEditorsRepositoryInterface import HardcodedTwitchChannelEditorsRepositoryInterface
from ..friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface
from ..officialAccounts.officialTwitchAccountUserIdProviderInterface import OfficialTwitchAccountUserIdProviderInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class HardcodedTwitchChannelEditorsRepository(HardcodedTwitchChannelEditorsRepositoryInterface):

    def __init__(
        self,
        officialTwitchAccountUserIdProvider: OfficialTwitchAccountUserIdProviderInterface,
        timber: TimberInterface,
        twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface,
    ):
        if not isinstance(officialTwitchAccountUserIdProvider, OfficialTwitchAccountUserIdProviderInterface):
            raise TypeError(f'officialTwitchAccountUserIdProvider argument is malformed: \"{officialTwitchAccountUserIdProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchFriendsUserIdRepository, TwitchFriendsUserIdRepositoryInterface):
            raise TypeError(f'twitchFriendsUserIdRepository argument is malformed: \"{twitchFriendsUserIdRepository}\"')

        self.__officialTwitchAccountUserIdProvider: Final[OfficialTwitchAccountUserIdProviderInterface] = officialTwitchAccountUserIdProvider
        self.__timber: Final[TimberInterface] = timber
        self.__twitchFriendsUserIdRepository: Final[TwitchFriendsUserIdRepositoryInterface] = twitchFriendsUserIdRepository

        self.__cache: Final[dict[str, frozenset[str] | None]] = dict()

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('HardcodedTwitchChannelEditorsRepository', 'Caches cleared')

    async def get(self, twitchChannelId: str) -> frozenset[str]:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        cachedValue = self.__cache.get(twitchChannelId, None)
        if cachedValue is not None:
            return cachedValue

        rawHardcodedEditorIds: Collection[str | None]

        if twitchChannelId == await self.__twitchFriendsUserIdRepository.getCharlyUserId():
            rawHardcodedEditorIds = await self.__getHardcodedCharlyEditorIds()
        else:
            rawHardcodedEditorIds = set()

        hardcodedEditorIds: set[str] = set()

        for hardcodedEditorId in rawHardcodedEditorIds:
            if utils.isValidStr(hardcodedEditorId):
                hardcodedEditorIds.add(hardcodedEditorId)

        frozenHardcodedEditorIds = frozenset(hardcodedEditorIds)
        self.__cache[twitchChannelId] = frozenHardcodedEditorIds
        return frozenHardcodedEditorIds

    async def __getHardcodedCharlyEditorIds(self) -> Collection[str | None]:
        return frozenset({
            await self.__officialTwitchAccountUserIdProvider.getCynanBotUserId(),
            await self.__twitchFriendsUserIdRepository.getBastionBlueUserId(),
            await self.__twitchFriendsUserIdRepository.getEddieUserId(),
            await self.__twitchFriendsUserIdRepository.getHarleyHardtUserId(),
            await self.__twitchFriendsUserIdRepository.getImytUserId(),
            await self.__twitchFriendsUserIdRepository.getTsteineUserId(),
        })
