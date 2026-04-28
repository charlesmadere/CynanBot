import re
import traceback
from typing import Any, Collection, Final, Pattern

from frozenlist import FrozenList

from .absChatCommand import AbsChatCommand
from .chatCommandResult import ChatCommandResult
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..misc.clearable import Clearable
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class ClearCachesChatCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        clearables: Collection[Clearable | Any | None] | None,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif clearables is not None and not isinstance(clearables, Collection):
            raise TypeError(f'clearables argument is malformed: \"{clearables}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

        self.__clearables: Final[Collection[Clearable]] = self.__buildClearablesCollection(clearables)

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!clearcaches?\b', re.IGNORECASE),
        })

    def __buildClearablesCollection(
        self,
        clearables: Collection[Clearable | Any | None] | None,
    ) -> Collection[Clearable]:
        if clearables is None:
            emptyClearables: FrozenList[Clearable] = FrozenList()
            emptyClearables.freeze()
            return emptyClearables

        frozenClearables: FrozenList[Clearable | Any | None] = FrozenList(clearables)
        frozenClearables.freeze()

        validClearables: FrozenList[Clearable] = FrozenList()

        for index, clearable in enumerate(frozenClearables):
            if clearable is None:
                continue
            elif isinstance(clearable, Clearable):
                validClearables.append(clearable)
            else:
                exception = TypeError(f'Encountered an invalid Clearable instance ({index=}) ({clearable=}) ({frozenClearables=})')
                self.__timber.log(self.commandName, f'Encountered an invalid Clearable instance ({index=}) ({clearable=}) ({frozenClearables=})', exception, traceback.format_exc())
                raise exception

        validClearables.freeze()
        return validClearables

    @property
    def commandName(self) -> str:
        return 'ClearCachesChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not await self.__hasPermissions(chatMessage):
            return ChatCommandResult.IGNORED

        for clearable in self.__clearables:
            await clearable.clearCaches()

        self.__twitchChatMessenger.send(
            text = 'ⓘ All caches cleared',
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )

        self.__timber.log(self.commandName, f'Handled ({chatMessage=})')
        return ChatCommandResult.CONSUMED

    async def __hasPermissions(self, chatMessage: TwitchChatMessage) -> bool:
        isAdministrator = chatMessage.chatterUserId == await self.__administratorProvider.getAdministratorUserId()
        return isAdministrator
