from typing import Collection, Final

from .hardcodedTwitchChannelEditorsRepositoryInterface import HardcodedTwitchChannelEditorsRepositoryInterface
from ..friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface
from ...misc import utils as utils


class HardcodedTwitchChannelEditorsRepository(HardcodedTwitchChannelEditorsRepositoryInterface):

    def __init__(
        self,
        twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface,
    ):
        if not isinstance(twitchFriendsUserIdRepository, TwitchFriendsUserIdRepositoryInterface):
            raise TypeError(f'twitchFriendsUserIdRepository argument is malformed: \"{twitchFriendsUserIdRepository}\"')

        self.__twitchFriendsUserIdRepository: Final[TwitchFriendsUserIdRepositoryInterface] = twitchFriendsUserIdRepository

    async def get(self, twitchChannelId: str) -> frozenset[str]:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        charlyUserId = await self.__twitchFriendsUserIdRepository.getCharlyUserId()
        rawHardcodedEditorIds: Collection[str | None] | None

        if twitchChannelId == charlyUserId:
            rawHardcodedEditorIds = await self.__getHardcodedCharlyEditorIds()
        else:
            rawHardcodedEditorIds = None

        hardcodedEditorIds: set[str] = set()

        if rawHardcodedEditorIds is not None:
            for hardcodedEditorId in rawHardcodedEditorIds:
                if utils.isValidStr(hardcodedEditorId):
                    hardcodedEditorIds.add(hardcodedEditorId)

        return frozenset(hardcodedEditorIds)

    async def __getHardcodedCharlyEditorIds(self) -> Collection[str | None]:
        return frozenset({
            await self.__twitchFriendsUserIdRepository.getBastionBlueUserId(),
            await self.__twitchFriendsUserIdRepository.getEddieUserId(),
            await self.__twitchFriendsUserIdRepository.getHarleyHardtUserId(),
            await self.__twitchFriendsUserIdRepository.getImytUserId(),
        })
