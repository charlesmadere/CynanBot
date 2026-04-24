import re
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..cheerActions.cheerActionsRepositoryInterface import CheerActionsRepositoryInterface
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class GetCheerActionsChatCommand(AbsChatCommand2):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        cheerActionsRepository: CheerActionsRepositoryInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(cheerActionsRepository, CheerActionsRepositoryInterface):
            raise TypeError(f'cheerActionsRepository argument is malformed: \"{cheerActionsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__cheerActionsRepository: Final[CheerActionsRepositoryInterface] = cheerActionsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!(?:get)?cheeractions?\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'GetCheerActionsChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not await self.__hasPermissions(
            chatMessage = chatMessage,
        ):
            return ChatCommandResult.IGNORED

        actions = await self.__cheerActionsRepository.getActions(
            twitchChannelId = chatMessage.twitchChannelId,
        )

        enabledOrDisabledState: str

        if chatMessage.twitchUser.areCheerActionsEnabled:
            enabledOrDisabledState = 'enabled'
        else:
            enabledOrDisabledState = 'disabled'

        if len(actions) == 0:
            self.__twitchChatMessenger.send(
                text = f'ⓘ You have no cheer actions (cheer actions are currently globally {enabledOrDisabledState} for your user)',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
        else:
            self.__twitchChatMessenger.send(
                text = f'ⓘ You have {len(actions)} cheer action(s) (cheer actions are currently globally {enabledOrDisabledState} for your user)',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            for action in actions.values():
                self.__twitchChatMessenger.send(
                    text = f'Action {action.getBits()} — {action.printOut()}',
                    twitchChannelId = chatMessage.twitchChannelId,
                    replyMessageId = chatMessage.twitchChatMessageId,
                )

        self.__timber.log(self.commandName, f'Handled ({actions=}) ({chatMessage=})')
        return ChatCommandResult.CONSUMED

    async def __hasPermissions(self, chatMessage: TwitchChatMessage) -> bool:
        isStreamer = chatMessage.chatterUserId == chatMessage.twitchChannelId
        isAdministrator = chatMessage.chatterUserId == await self.__administratorProvider.getAdministratorUserId()
        return isStreamer or isAdministrator
