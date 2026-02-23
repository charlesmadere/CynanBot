import re
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..mouseCursor.mouseCursorHelperInterface import MouseCursorHelperInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class TestMouseCursorChatCommand(AbsChatCommand2):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        mouseCursorHelper: MouseCursorHelperInterface,
        timber: TimberInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(mouseCursorHelper, MouseCursorHelperInterface):
            raise TypeError(f'mouseCursorHelper argument is malformed: \"{mouseCursorHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__mouseCursorHelper: Final[MouseCursorHelperInterface] = mouseCursorHelper
        self.__timber: Final[TimberInterface] = timber

        self.__commandPatterns: Final[frozenset[Pattern]] = frozenset({
            re.compile(r'\s*!testmousecursor\.*', re.IGNORECASE),
            re.compile(r'\s*!testmousepointer\.*', re.IGNORECASE),
        })

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isMouseCursorEnabled:
            return ChatCommandResult.IGNORED

        administratorUserId = await self.__administratorProvider.getAdministratorUserId()
        if chatMessage.chatterUserId != administratorUserId:
            return ChatCommandResult.IGNORED

        result = await self.__mouseCursorHelper.applyMouseCursor(
            twitchChannel = chatMessage.twitchChannel,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        self.__timber.log('TestMouseCursorChatCommand', f'Result ({chatMessage=}) ({result=})')
        return ChatCommandResult.HANDLED
