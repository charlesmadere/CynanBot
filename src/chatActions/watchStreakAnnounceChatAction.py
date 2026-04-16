from typing import Final

from .absChatAction import AbsChatAction
from .chatActionResult import ChatActionResult
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..timber.timberInterface import TimberInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage
from ..watchStreaks.helper.watchStreaksHelperInterface import WatchStreaksHelperInterface
from ..watchStreaks.models.watchStreakTtsAnnouncementResult import WatchStreakTtsAnnouncementResult


class WatchStreakAnnounceChatAction(AbsChatAction):

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
        return 'WatchStreakAnnounceChatAction'

    async def handleChatAction(
        self,
        mostRecentChat: MostRecentChat | None,
        chatMessage: TwitchChatMessage,
    ) -> ChatActionResult:
        if not chatMessage.twitchUser.isWatchStreakTtsAnnounceEnabled:
            return ChatActionResult.IGNORED
        elif chatMessage.watchStreak is None or chatMessage.watchStreak.streakCount < 1:
            return ChatActionResult.IGNORED

        result = await self.__watchStreaksHelper.watchStreakTtsAnnounce(
            watchStreak = chatMessage.watchStreak.streakCount,
            chatterUserId = chatMessage.chatterUserId,
            chatterUserName = chatMessage.chatterUserName,
            twitchChannelId = chatMessage.twitchChannelId,
            user = chatMessage.twitchUser,
        )

        if result is not WatchStreakTtsAnnouncementResult.SUBMITTED_TTS_EVENT:
            return ChatActionResult.IGNORED

        self.__timber.log(self.actionName, f'Submitted watch streak TTS announcement ({result=}) ({chatMessage=})')
        return ChatActionResult.CONSUMED
