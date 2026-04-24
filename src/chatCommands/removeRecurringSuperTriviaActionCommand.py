import re
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..recurringActions.recurringActionsHelperInterface import \
    RecurringActionsHelperInterface
from ..recurringActions.recurringActionsRepositoryInterface import \
    RecurringActionsRepositoryInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class RemoveRecurringSuperTriviaActionCommand(AbsChatCommand2):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        recurringActionsHelper: RecurringActionsHelperInterface,
        recurringActionsRepository: RecurringActionsRepositoryInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(recurringActionsHelper, RecurringActionsHelperInterface):
            raise TypeError(f'recurringActionsHelper argument is malformed: \"{recurringActionsHelper}\"')
        elif not isinstance(recurringActionsRepository, RecurringActionsRepositoryInterface):
            raise TypeError(f'recurringActionsRepository argument is malformed: \"{recurringActionsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__recurringActionsHelper: Final[RecurringActionsHelperInterface] = recurringActionsHelper
        self.__recurringActionsRepository: Final[RecurringActionsRepositoryInterface] = recurringActionsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!del(?:ete)?recurringsupertrivia(?:action)?\b', re.IGNORECASE),
            re.compile(r'^\s*!removerecurringsupertrivia(?:action)?\b', re.IGNORECASE),
            re.compile(r'^\s*!rmrecurringsupertrivia(?:action)?\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'RemoveRecurringSuperTriviaActionCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.areRecurringActionsEnabled:
            return ChatCommandResult.IGNORED
        elif not await self.__hasPermissions(chatMessage):
            return ChatCommandResult.IGNORED

        recurringAction = await self.__recurringActionsRepository.getSuperTriviaRecurringAction(
            twitchChannel = chatMessage.twitchChannel,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        if recurringAction is None:
            self.__twitchChatMessenger.send(
                text = f'⚠ Your channel has no recurring super trivia action',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

        elif not recurringAction.isEnabled:
            self.__twitchChatMessenger.send(
                text = f'⚠ Your channel\'s recurring super trivia action is already disabled',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

        else:
            await self.__recurringActionsHelper.disableRecurringAction(
                recurringAction = recurringAction,
            )

            self.__twitchChatMessenger.send(
                text = f'ⓘ Recurring super trivia action has been disabled',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

        self.__timber.log(self.commandName, f'Handled ({recurringAction=}) ({chatMessage=})')
        return ChatCommandResult.CONSUMED

    async def __hasPermissions(self, chatMessage: TwitchChatMessage) -> bool:
        isStreamer = chatMessage.chatterUserId == chatMessage.twitchChannelId
        isAdministrator = chatMessage.chatterUserId == await self.__administratorProvider.getAdministratorUserId()
        return isStreamer or isAdministrator
