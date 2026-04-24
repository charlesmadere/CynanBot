import re
from typing import Collection, Final, Pattern

from frozenlist import FrozenList

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..recurringActions.actions.recurringAction import RecurringAction
from ..recurringActions.recurringActionsRepositoryInterface import RecurringActionsRepositoryInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class GetRecurringActionsChatCommand(AbsChatCommand2):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        recurringActionsRepository: RecurringActionsRepositoryInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        delimiter: str = ', ',
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(recurringActionsRepository, RecurringActionsRepositoryInterface):
            raise TypeError(f'recurringActionsRepository argument is malformed: \"{recurringActionsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__recurringActionsRepository: Final[RecurringActionsRepositoryInterface] = recurringActionsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__delimiter: Final[str] = delimiter

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!(?:get)?recurringactions?\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'GetRecurringActionsChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not await self.__hasPermissions(chatMessage):
            return ChatCommandResult.IGNORED

        recurringActions = await self.__recurringActionsRepository.getAllRecurringActions(
            twitchChannel = chatMessage.twitchChannel,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        self.__twitchChatMessenger.send(
            text = await self.__toStr(recurringActions),
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )

        self.__timber.log(self.commandName, f'Handled ({chatMessage=})')
        return ChatCommandResult.CONSUMED

    async def __hasPermissions(self, chatMessage: TwitchChatMessage) -> bool:
        isStreamer = chatMessage.chatterUserId == chatMessage.twitchChannelId
        isAdministrator = chatMessage.chatterUserId == await self.__administratorProvider.getAdministratorUserId()
        return isStreamer or isAdministrator

    async def __toStr(self, recurringActions: FrozenList[RecurringAction]) -> str:
        if not isinstance(recurringActions, list):
            raise TypeError(f'recurringActions argument is malformed: \"{recurringActions}\"')

        if len(recurringActions) == 0:
            return 'ⓘ Your channel has no recurring actions'

        recurringActionsStrs: list[str] = list()

        for recurringAction in recurringActions:
            recurringActionsStrs.append(recurringAction.actionType.humanReadableString)

        recurringActionsStr = self.__delimiter.join(recurringActionsStrs)
        return f'ⓘ Your channel\'s recurring action(s): {recurringActionsStr}'
