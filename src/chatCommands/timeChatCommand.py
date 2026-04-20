import re
from datetime import datetime
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class TimeChatCommand(AbsChatCommand2):

    def __init__(
        self,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!time(?:zone)?\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'TimeChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        timeZones = chatMessage.twitchUser.timeZones
        if timeZones is None or len(timeZones) == 0:
            return ChatCommandResult.IGNORED

        first = True
        text = ''

        for timeZone in timeZones:
            localTime = datetime.now(timeZone)

            if first:
                first = False
                formattedTime = utils.formatTime(localTime)
                text = f'🕰️ The stream\'s local time is {formattedTime}.'
            else:
                formattedTime = utils.formatTimeShort(localTime)
                timeZoneName = localTime.strftime('%Z')
                text = f'{text} {timeZoneName} time is {formattedTime}.'

        self.__twitchChatMessenger.send(
            text = text,
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )

        self.__timber.log(self.commandName, f'Handled ({timeZones=}) ({chatMessage=})')
        return ChatCommandResult.CONSUMED
