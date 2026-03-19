import re
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..cuteness.cutenessPresenterInterface import CutenessPresenterInterface
from ..cuteness.cutenessRepositoryInterface import CutenessRepositoryInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class CutenessChampionsChatCommand(AbsChatCommand2):

    def __init__(
        self,
        cutenessPresenter: CutenessPresenterInterface,
        cutenessRepository: CutenessRepositoryInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(cutenessPresenter, CutenessPresenterInterface):
            raise TypeError(f'cutenessPresenter argument is malformed: \"{cutenessPresenter}\"')
        if not isinstance(cutenessRepository, CutenessRepositoryInterface):
            raise TypeError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__cutenessPresenter: Final[CutenessPresenterInterface] = cutenessPresenter
        self.__cutenessRepository: Final[CutenessRepositoryInterface] = cutenessRepository
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!cutenesschamps\b', re.IGNORECASE),
            re.compile(r'^\s*!cutenesschampions\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'CutenessChampionsChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isCutenessEnabled:
            return ChatCommandResult.IGNORED

        result = await self.__cutenessRepository.fetchCutenessChampions(
            twitchChannel = chatMessage.twitchChannel,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        printOut = await self.__cutenessPresenter.printCutenessChampions(
            result = result,
        )

        self.__twitchChatMessenger.send(
            text = printOut,
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )

        self.__timber.log(self.commandName, f'Handled ({result=})')
        return ChatCommandResult.HANDLED
