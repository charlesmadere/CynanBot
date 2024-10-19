from datetime import datetime, timedelta

from .trollmojiHelperInterface import TrollmojiHelperInterface
from .trollmojiSettingsRepositoryInterface import TrollmojiSettingsRepositoryInterface
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.emotes.twitchEmotesHelperInterface import TwitchEmotesHelperInterface
from ..twitch.friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface


class TrollmojiHelper(TrollmojiHelperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        trollmojiSettingsRepository: TrollmojiSettingsRepositoryInterface,
        twitchEmotesHelper: TwitchEmotesHelperInterface,
        twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface,
        cacheTimeBuffer: timedelta = timedelta(hours = 3)
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchEmotesHelper, TwitchEmotesHelperInterface):
            raise TypeError(f'twitchEmotesHelper argument is malformed: \"{twitchEmotesHelper}\"')
        elif not isinstance(twitchFriendsUserIdRepository, TwitchFriendsUserIdRepositoryInterface):
            raise TypeError(f'twitchFriendsUserIdRepository argument is malformed: \"{twitchFriendsUserIdRepository}\"')
        elif not isinstance(cacheTimeBuffer, timedelta):
            raise TypeError(f'cacheTimeBuffer argument is malformed: \"{cacheTimeBuffer}\"')

        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__trollmojiSettingsRepository: TrollmojiSettingsRepositoryInterface = trollmojiSettingsRepository
        self.__twitchEmotesHelper: TwitchEmotesHelperInterface = twitchEmotesHelper
        self.__twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface = twitchFriendsUserIdRepository
        self.__cacheTimeBuffer: timedelta = cacheTimeBuffer

    async def clearCaches(self):
        # TODO
        pass

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

        # TODO
        return None

    async def getGottemEmote(self) -> str | None:
        gottemEmote = await self.__trollmojiSettingsRepository.getGottemEmote()

        if gottemEmote is None:
            return None

        return self.getEmote(
            emoteText = gottemEmote.emoteText,
            twitchEmoteChannelId = gottemEmote.twitchChannelId
        )

    async def getHypeEmote(self) -> str | None:
        hypeEmote = await self.__trollmojiSettingsRepository.getHypeEmote()

        if hypeEmote is None:
            return None

        return self.getEmote(
            emoteText = hypeEmote.emoteText,
            twitchEmoteChannelId = hypeEmote.twitchChannelId
        )
