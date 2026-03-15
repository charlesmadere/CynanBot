import locale
import re
from dataclasses import dataclass
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..timber.timberInterface import TimberInterface
from ..twitch.activeChatters.activeChatter import ActiveChatter
from ..twitch.activeChatters.activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage
from ..twitch.timeout.timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface


class VulnerableChattersChatCommand(AbsChatCommand2):

    @dataclass(frozen = True, slots = True)
    class VulnerableChattersData:
        totalActiveChatters: int
        totalVulnerableChatters: int

        @property
        def totalActiveChattersStr(self) -> str:
            return locale.format_string("%d", self.totalActiveChatters, grouping = True)

        @property
        def totalVulnerableChattersStr(self) -> str:
            return locale.format_string("%d", self.totalVulnerableChatters, grouping = True)

    def __init__(
        self,
        activeChattersRepository: ActiveChattersRepositoryInterface,
        timber: TimberInterface,
        timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(activeChattersRepository, ActiveChattersRepositoryInterface):
            raise TypeError(f'activeChattersRepository argument is malformed: \"{activeChattersRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__activeChattersRepository: Final[ActiveChattersRepositoryInterface] = activeChattersRepository
        self.__timber: Final[TimberInterface] = timber
        self.__timeoutImmuneUserIdsRepository: Final[TimeoutImmuneUserIdsRepositoryInterface] = timeoutImmuneUserIdsRepository
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!vcs?\b', re.IGNORECASE),
            re.compile(r'^\s*!vulnerablechatters?\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'VulnerableChattersChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def __getVulnerableChattersData(self, twitchChannelId: str) -> VulnerableChattersData:
        activeChatters = await self.__activeChattersRepository.get(
            twitchChannelId = twitchChannelId,
        )

        vulnerableChatters: dict[str, ActiveChatter] = dict(activeChatters)
        vulnerableChatters.pop(twitchChannelId, None)

        allImmuneUserIds = await self.__timeoutImmuneUserIdsRepository.getAllUserIds()

        for immuneUserId in allImmuneUserIds:
            vulnerableChatters.pop(immuneUserId, None)

        return VulnerableChattersChatCommand.VulnerableChattersData(
            totalActiveChatters = len(activeChatters),
            totalVulnerableChatters = len(vulnerableChatters),
        )

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isVulnerableChattersEnabled:
            return ChatCommandResult.IGNORED

        chattersData = await self.__getVulnerableChattersData(
            twitchChannelId = chatMessage.twitchChannelId,
        )

        message = f'ⓘ There are {chattersData.totalVulnerableChattersStr} vulnerable chatter(s) and {chattersData.totalActiveChattersStr} active chatter(s)'

        self.__twitchChatMessenger.send(
            text = message,
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )

        self.__timber.log(self.commandName, f'Handled ({chattersData=})')
        return ChatCommandResult.HANDLED
