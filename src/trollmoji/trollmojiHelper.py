from datetime import datetime, timedelta
from typing import Final

from .trollmojiHelperInterface import TrollmojiHelperInterface
from .trollmojiSettingsRepositoryInterface import TrollmojiSettingsRepositoryInterface
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.emotes.twitchEmotesHelperInterface import TwitchEmotesHelperInterface


class TrollmojiHelper(TrollmojiHelperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        trollmojiSettingsRepository: TrollmojiSettingsRepositoryInterface,
        twitchEmotesHelper: TwitchEmotesHelperInterface,
        cacheTimeBuffer: timedelta = timedelta(hours = 3)
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchEmotesHelper, TwitchEmotesHelperInterface):
            raise TypeError(f'twitchEmotesHelper argument is malformed: \"{twitchEmotesHelper}\"')
        elif not isinstance(cacheTimeBuffer, timedelta):
            raise TypeError(f'cacheTimeBuffer argument is malformed: \"{cacheTimeBuffer}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__trollmojiSettingsRepository: Final[TrollmojiSettingsRepositoryInterface] = trollmojiSettingsRepository
        self.__twitchEmotesHelper: Final[TwitchEmotesHelperInterface] = twitchEmotesHelper
        self.__cacheTimeBuffer: Final[timedelta] = cacheTimeBuffer

        self.__isAvailableCache: Final[dict[str, bool | None]] = dict()
        self.__timeCache: Final[dict[str, datetime | None]] = dict()

    async def clearCaches(self):
        self.__isAvailableCache.clear()
        self.__timeCache.clear()
        self.__timber.log('TrollmojiHelper', 'Caches cleared')

    async def getBombEmote(self) -> str | None:
        bombEmote = await self.__trollmojiSettingsRepository.getBombEmote()

        if bombEmote is None:
            return None

        return await self.getEmote(
            emoteText = bombEmote.emoteText,
            twitchEmoteChannelId = bombEmote.twitchChannelId
        )

    async def getBombEmoteOrBackup(self) -> str:
        bombEmote = await self.getBombEmote()

        if utils.isValidStr(bombEmote):
            return bombEmote
        else:
            return await self.__trollmojiSettingsRepository.getBombEmoteBackup()

    async def getDinkDonkEmote(self) -> str | None:
        dinkDonkEmote = await self.__trollmojiSettingsRepository.getDinkDonkEmote()

        if dinkDonkEmote is None:
            return None

        return await self.getEmote(
            emoteText = dinkDonkEmote.emoteText,
            twitchEmoteChannelId = dinkDonkEmote.twitchChannelId
        )

    async def getEmote(
        self,
        emoteText: str | None,
        twitchEmoteChannelId: str
    ) -> str | None:
        if emoteText is not None and not isinstance(emoteText, str):
            raise TypeError(f'emoteText argument is malformed: \"{emoteText}\"')
        elif not utils.isValidStr(twitchEmoteChannelId):
            raise TypeError(f'twitchEmoteChannelId argument is malformed: \"{twitchEmoteChannelId}\"')

        if not utils.isValidStr(emoteText):
            return None

        isAvailable = self.__isAvailableCache.get(emoteText, False)
        cachedTime = self.__timeCache.get(emoteText, None)
        now = datetime.now(self.__timeZoneRepository.getDefault())

        if cachedTime is not None and cachedTime >= now:
            if isAvailable:
                return emoteText
            else:
                return None

        viableEmoteNames = await self.__twitchEmotesHelper.fetchViableSubscriptionEmoteNames(
            twitchChannelId = twitchEmoteChannelId
        )

        emoteIsAvailable = emoteText in viableEmoteNames
        self.__isAvailableCache[emoteText] = emoteIsAvailable
        self.__timeCache[emoteText] = now + self.__cacheTimeBuffer

        if emoteIsAvailable:
            self.__timber.log('TriviaTwitchEmoteHelper', f'Emote is available ({emoteText=}) ({twitchEmoteChannelId=})')
            return emoteText
        else:
            self.__timber.log('TriviaTwitchEmoteHelper', f'Emote isn\'t available ({emoteText=}) ({twitchEmoteChannelId=})')
            return None

    async def getExplodedEmote(self) -> str | None:
        explodedEmote = await self.__trollmojiSettingsRepository.getExplodedEmote()

        if explodedEmote is None:
            return None

        return await self.getEmote(
            emoteText = explodedEmote.emoteText,
            twitchEmoteChannelId = explodedEmote.twitchChannelId
        )

    async def getExplodedEmoteOrBackup(self) -> str:
        explodedEmote = await self.getExplodedEmote()

        if utils.isValidStr(explodedEmote):
            return explodedEmote
        else:
            return await self.__trollmojiSettingsRepository.getExplodedEmoteBackup()

    async def getGottemEmote(self) -> str | None:
        gottemEmote = await self.__trollmojiSettingsRepository.getGottemEmote()

        if gottemEmote is None:
            return None

        return await self.getEmote(
            emoteText = gottemEmote.emoteText,
            twitchEmoteChannelId = gottemEmote.twitchChannelId
        )

    async def getGottemEmoteOrBackup(self) -> str:
        gottemEmote = await self.getGottemEmote()

        if utils.isValidStr(gottemEmote):
            return gottemEmote
        else:
            return await self.__trollmojiSettingsRepository.getGottemEmoteBackup()

    async def getHypeEmote(self) -> str | None:
        hypeEmote = await self.__trollmojiSettingsRepository.getHypeEmote()

        if hypeEmote is None:
            return None

        return await self.getEmote(
            emoteText = hypeEmote.emoteText,
            twitchEmoteChannelId = hypeEmote.twitchChannelId
        )

    async def getHypeEmoteOrBackup(self) -> str:
        hypeEmote = await self.getHypeEmote()

        if utils.isValidStr(hypeEmote):
            return hypeEmote
        else:
            return await self.__trollmojiSettingsRepository.getHypeEmoteBackup()

    async def getShrugEmote(self) -> str | None:
        shrugEmote = await self.__trollmojiSettingsRepository.getShrugEmote()

        if shrugEmote is None:
            return None

        return await self.getEmote(
            emoteText = shrugEmote.emoteText,
            twitchEmoteChannelId = shrugEmote.twitchChannelId
        )

    async def getThumbsDownEmote(self) -> str | None:
        thumbsDownEmote = await self.__trollmojiSettingsRepository.getThumbsDownEmote()

        if thumbsDownEmote is None:
            return None

        return await self.getEmote(
            emoteText = thumbsDownEmote.emoteText,
            twitchEmoteChannelId = thumbsDownEmote.twitchChannelId
        )

    async def getThumbsDownEmoteOrBackup(self) -> str:
        thumbsDownEmote = await self.getThumbsDownEmote()

        if utils.isValidStr(thumbsDownEmote):
            return thumbsDownEmote
        else:
            return await self.__trollmojiSettingsRepository.getThumbsDownEmoteBackup()

    async def getThumbsUpEmote(self) -> str | None:
        thumbsUpEmote = await self.__trollmojiSettingsRepository.getThumbsUpEmote()

        if thumbsUpEmote is None:
            return None

        return await self.getEmote(
            emoteText = thumbsUpEmote.emoteText,
            twitchEmoteChannelId = thumbsUpEmote.twitchChannelId
        )

    async def getThumbsUpEmoteOrBackup(self) -> str:
        thumbsUpEmote = await self.getThumbsUpEmote()

        if utils.isValidStr(thumbsUpEmote):
            return thumbsUpEmote
        else:
            return await self.__trollmojiSettingsRepository.getThumbsUpEmoteBackup()
