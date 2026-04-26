import re
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..asplodieStats.asplodieStatsPresenter import AsplodieStatsPresenter
from ..asplodieStats.repository.asplodieStatsRepositoryInterface import AsplodieStatsRepositoryInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class AsplodieStatsChatCommand(AbsChatCommand2):

    def __init__(
        self,
        asplodieStatsPresenter: AsplodieStatsPresenter,
        asplodieStatsRepository: AsplodieStatsRepositoryInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        userIdsRepository: UserIdsRepositoryInterface,
    ):
        if not isinstance(asplodieStatsPresenter, AsplodieStatsPresenter):
            raise TypeError(f'asplodieStatsPresenter argument is malformed: \"{asplodieStatsPresenter}\"')
        elif not isinstance(asplodieStatsRepository, AsplodieStatsRepositoryInterface):
            raise TypeError(f'asplodieStatsRepository argument is malformed: \"{asplodieStatsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__asplodieStatsPresenter: Final[AsplodieStatsPresenter] = asplodieStatsPresenter
        self.__asplodieStatsRepository: Final[AsplodieStatsRepositoryInterface] = asplodieStatsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!(?:my)?asplodiestats\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'AsplodieStatsChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.areAsplodieStatsEnabled:
            return ChatCommandResult.IGNORED

        asplodieStats = await self.__asplodieStatsRepository.get(
            chatterUserId = chatMessage.chatterUserId,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        printOut = await self.__asplodieStatsPresenter.printOut(
            asplodieStats = asplodieStats,
        )

        self.__twitchChatMessenger.send(
            text = f'ⓘ Your asplodie stats — {printOut}',
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )

        self.__timber.log(self.commandName, f'Handled ({asplodieStats=}) ({chatMessage=})')
        return ChatCommandResult.CONSUMED
