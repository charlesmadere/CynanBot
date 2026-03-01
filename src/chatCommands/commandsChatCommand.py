import re
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class CommandsChatCommand(AbsChatCommand2):

    def __init__(
        self,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        commandsUrl: str = 'https://cynanbot.io',
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not utils.isValidUrl(commandsUrl):
            raise TypeError(f'commandsUrl argument is malformed: \"{commandsUrl}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__commandsUrl: Final[str] = commandsUrl

        self.__commandPatterns: Final[frozenset[Pattern]] = frozenset({
            re.compile(r'^\s*!commands?', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'CommandsChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isCommandsCommandEnabled:
            return ChatCommandResult.IGNORED

        self.__twitchChatMessenger.send(
            text = f'ⓘ Commands: {self.__commandsUrl}',
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )

        self.__timber.log(self.commandName, f'Result ({chatMessage=})')
        return ChatCommandResult.HANDLED
