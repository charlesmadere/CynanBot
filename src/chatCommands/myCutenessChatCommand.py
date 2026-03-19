import re
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..cuteness.cutenessRepositoryInterface import CutenessRepositoryInterface
from ..cuteness.cutenessUtilsInterface import CutenessUtilsInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class MyCutenessChatCommand(AbsChatCommand2):

    def __init__(
        self,
        cutenessRepository: CutenessRepositoryInterface,
        cutenessUtils: CutenessUtilsInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(cutenessRepository, CutenessRepositoryInterface):
            raise TypeError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif not isinstance(cutenessUtils, CutenessUtilsInterface):
            raise TypeError(f'cutenessUtils argument is malformed: \"{cutenessUtils}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__cutenessRepository: Final[CutenessRepositoryInterface] = cutenessRepository
        self.__cutenessUtils: Final[CutenessUtilsInterface] = cutenessUtils
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!mycuteness(?:history)?\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'MyCutenessChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isCutenessEnabled:
            return ChatCommandResult.IGNORED

        result = await self.__cutenessRepository.fetchCutenessHistory(
            twitchChannel = chatMessage.twitchChannel,
            twitchChannelId = chatMessage.twitchChannelId,
            userId = chatMessage.chatterUserId,
            userName = chatMessage.chatterUserName,
        )

        message = self.__cutenessUtils.getCutenessHistory(
            result = result,
        )

        self.__twitchChatMessenger.send(
            text = message,
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )

        self.__timber.log(self.commandName, f'Handled ({result=})')
        return ChatCommandResult.HANDLED
