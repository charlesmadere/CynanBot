from .trollmojiDetails import TrollmojiDetails
from .trollmojiSettingsRepositoryInterface import TrollmojiSettingsRepositoryInterface
from ..misc import utils as utils
from ..twitch.friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface


class TrollmojiSettingsRepository(TrollmojiSettingsRepositoryInterface):

    def __init__(
        self,
        twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface,
        gottemEmoteBackup: str = 'RIPBOZO'
    ):
        if not isinstance(twitchFriendsUserIdRepository, TwitchFriendsUserIdRepositoryInterface):
            raise TypeError(f'twitchFriendsUserIdRepository argument is malformed: \"{twitchFriendsUserIdRepository}\"')
        elif not utils.isValidStr(gottemEmoteBackup):
            raise TypeError(f'gottemEmoteBackup argument is malformed: \"{gottemEmoteBackup}\"')

        self.__twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface = twitchFriendsUserIdRepository
        self.__gottemEmoteBackup: str = gottemEmoteBackup

    async def clearCaches(self):
        # this method is intentionally empty
        pass

    async def getGottemEmote(self) -> TrollmojiDetails | None:
        return await self.__getSamusEmote('samusGOTTEM')

    async def getGottemEmoteBackup(self) -> str:
        return self.__gottemEmoteBackup

    async def getHypeEmote(self) -> TrollmojiDetails | None:
        return await self.__getSamusEmote('samusHype')

    async def __getSamusEmote(
        self,
        emoteText: str | None
    ) -> TrollmojiDetails | None:
        if not utils.isValidStr(emoteText):
            return None

        twitchChannelId = await self.__twitchFriendsUserIdRepository.getCharlesUserId()
        if not utils.isValidStr(twitchChannelId):
            return None

        return TrollmojiDetails(
            emoteText = emoteText,
            twitchChannelId = twitchChannelId
        )

    async def getShrugEmote(self) -> TrollmojiDetails | None:
        return await self.__getSamusEmote('samusShrug')

    async def getThumbsDownEmote(self) -> TrollmojiDetails | None:
        return await self.__getSamusEmote('samusBad')

    async def getThumbsUpEmote(self) -> TrollmojiDetails | None:
        return await self.__getSamusEmote('samusGood')
