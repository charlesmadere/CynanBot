from typing import Final

from .absChatAction import AbsChatAction
from .chatActionResult import ChatActionResult
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..timber.timberInterface import TimberInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage
from ..watchStreaks.helper.watchStreaksHelperInterface import WatchStreaksHelperInterface
from ..watchStreaks.models.announceWatchStreakResult import AnnounceWatchStreakResult


class WatchStreakChatAction(AbsChatAction):

    def __init__(
        self,
        timber: TimberInterface,
        watchStreaksHelper: WatchStreaksHelperInterface,
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(watchStreaksHelper, WatchStreaksHelperInterface):
            raise TypeError(f'watchStreaksHelper argument is malformed: \"{watchStreaksHelper}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__watchStreaksHelper: Final[WatchStreaksHelperInterface] = watchStreaksHelper

    @property
    def actionName(self) -> str:
        return 'WatchStreakChatAction'

    async def handleChatAction(
        self,
        mostRecentChat: MostRecentChat | None,
        chatMessage: TwitchChatMessage,
    ) -> ChatActionResult:
        if chatMessage.watchStreak is None or chatMessage.watchStreak.streakCount < 1:
            return ChatActionResult.IGNORED

        announceResult = await self.__watchStreaksHelper.announceWatchStreak(
            watchStreak = chatMessage.watchStreak.streakCount,
            chatterUserId = chatMessage.chatterUserId,
            chatterUserLogin = chatMessage.chatterUserLogin,
            chatterUserName = chatMessage.chatterUserName,
            twitchChannelId = chatMessage.twitchChannelId,
            user = chatMessage.twitchUser,
        )

        streakStats = await self.__watchStreaksHelper.updateWatchStreakStats(
            watchStreak = chatMessage.watchStreak.streakCount,
            chatterUserId = chatMessage.chatterUserId,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        if announceResult is AnnounceWatchStreakResult.SUBMITTED_TTS_EVENT:
            self.__timber.log(self.actionName, f'Consumed watch streak ({announceResult=}) ({streakStats=}) ({chatMessage=})')
            return ChatActionResult.CONSUMED
        else:
            self.__timber.log(self.actionName, f'Handled watch streak ({announceResult=}) ({streakStats=}) ({chatMessage=})')
            return ChatActionResult.HANDLED
