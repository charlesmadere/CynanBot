from typing import Final

from .trollmojiDetails import TrollmojiDetails
from .trollmojiSettingsRepositoryInterface import TrollmojiSettingsRepositoryInterface
from ..misc import utils as utils
from ..twitch.friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface


class TrollmojiSettingsRepository(TrollmojiSettingsRepositoryInterface):

    def __init__(
        self,
        twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface,
        bombEmoteBackup: str = '💣',
        explodedEmoteBackup: str = '💥',
        gottemEmoteBackup: str = 'RIPBOZO',
        hypeEmoteBackup: str = '🎉',
        thumbsDownEmoteBackup: str = '👎',
        thumbsUpEmoteBackup: str = '👍',
    ):
        if not isinstance(twitchFriendsUserIdRepository, TwitchFriendsUserIdRepositoryInterface):
            raise TypeError(f'twitchFriendsUserIdRepository argument is malformed: \"{twitchFriendsUserIdRepository}\"')
        elif not utils.isValidStr(bombEmoteBackup):
            raise TypeError(f'bombEmoteBackup argument is malformed: \"{bombEmoteBackup}\"')
        elif not utils.isValidStr(explodedEmoteBackup):
            raise TypeError(f'explodedEmoteBackup argument is malformed: \"{explodedEmoteBackup}\"')
        elif not utils.isValidStr(gottemEmoteBackup):
            raise TypeError(f'gottemEmoteBackup argument is malformed: \"{gottemEmoteBackup}\"')
        elif not utils.isValidStr(hypeEmoteBackup):
            raise TypeError(f'hypeEmoteBackup argument is malformed: \"{hypeEmoteBackup}\"')
        elif not utils.isValidStr(thumbsDownEmoteBackup):
            raise TypeError(f'thumbsDownEmoteBackup argument is malformed: \"{thumbsDownEmoteBackup}\"')
        elif not utils.isValidStr(thumbsUpEmoteBackup):
            raise TypeError(f'thumbsUpEmoteBackup argument is malformed: \"{thumbsUpEmoteBackup}\"')

        self.__twitchFriendsUserIdRepository: Final[TwitchFriendsUserIdRepositoryInterface] = twitchFriendsUserIdRepository
        self.__bombEmoteBackup: Final[str] = bombEmoteBackup
        self.__explodedEmoteBackup: Final[str] = explodedEmoteBackup
        self.__gottemEmoteBackup: Final[str] = gottemEmoteBackup
        self.__hypeEmoteBackup: Final[str] = hypeEmoteBackup
        self.__thumbsDownEmoteBackup: Final[str] = thumbsDownEmoteBackup
        self.__thumbsUpEmoteBackup: Final[str] = thumbsUpEmoteBackup

    async def clearCaches(self):
        # this method is intentionally empty
        pass

    async def getBombEmote(self) -> TrollmojiDetails | None:
        return await self.__getMandoooEmote('mandoooTNT')

    async def getBombEmoteBackup(self) -> str:
        return self.__bombEmoteBackup

    async def getDinkDonkEmote(self) -> TrollmojiDetails | None:
        return await self.__getSamusEmote('samusDinkDonk')

    async def getExplodedEmote(self) -> TrollmojiDetails | None:
        return await self.__getSamusEmote('samusAsplodies')

    async def getExplodedEmoteBackup(self) -> str:
        return self.__explodedEmoteBackup

    async def getGottemEmote(self) -> TrollmojiDetails | None:
        return await self.__getSamusEmote('samusGOTTEM')

    async def getGottemEmoteBackup(self) -> str:
        return self.__gottemEmoteBackup

    async def getHypeEmote(self) -> TrollmojiDetails | None:
        return await self.__getSamusEmote('samusHype')

    async def getHypeEmoteBackup(self) -> str:
        return self.__hypeEmoteBackup

    async def __getMandoooEmote(
        self,
        emoteText: str | None
    ) -> TrollmojiDetails | None:
        if not utils.isValidStr(emoteText):
            return None

        twitchChannelId = await self.__twitchFriendsUserIdRepository.getEddieUserId()
        if not utils.isValidStr(twitchChannelId):
            return None

        return TrollmojiDetails(
            emoteText = emoteText,
            twitchChannelId = twitchChannelId,
        )

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
            twitchChannelId = twitchChannelId,
        )

    async def getShrugEmote(self) -> TrollmojiDetails | None:
        return await self.__getSamusEmote('samusShrug')

    async def getThumbsDownEmote(self) -> TrollmojiDetails | None:
        return await self.__getSamusEmote('samusBad')

    async def getThumbsDownEmoteBackup(self) -> str:
        return self.__thumbsDownEmoteBackup

    async def getThumbsUpEmote(self) -> TrollmojiDetails | None:
        return await self.__getSamusEmote('samusGood')

    async def getThumbsUpEmoteBackup(self) -> str:
        return self.__thumbsUpEmoteBackup
