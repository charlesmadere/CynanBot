import re
import traceback
from dataclasses import dataclass
from typing import Collection, Final, Pattern

from .absChatCommand import AbsChatCommand
from .chatCommandResult import ChatCommandResult
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..trivia.gameController.exceptions import TriviaGameControllerAlreadyExistsException
from ..trivia.gameController.triviaGameControllersHelperInterface import TriviaGameControllersHelperInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage
from ..twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ..twitch.userIds.twitchUserIdsHelperInterface import TwitchUserIdsHelperInterface


class AddGlobalTriviaControllerChatCommand(AbsChatCommand):

    @dataclass(frozen = True, slots = True)
    class Arguments:
        chatterUserId: str
        chatterUserLogin: str
        chatterUserName: str

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        timber: TimberInterface,
        triviaGameControllersHelper: TriviaGameControllersHelperInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        twitchUserIdsHelper: TwitchUserIdsHelperInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameControllersHelper, TriviaGameControllersHelperInterface):
            raise TypeError(f'triviaGameControllersHelper argument is malformed: \"{triviaGameControllersHelper}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(twitchUserIdsHelper, TwitchUserIdsHelperInterface):
            raise TypeError(f'twitchUserIdsHelper argument is malformed: \"{twitchUserIdsHelper}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__timber: Final[TimberInterface] = timber
        self.__triviaGameControllersHelper: Final[TriviaGameControllersHelperInterface] = triviaGameControllersHelper
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__twitchUserIdsHelper: Final[TwitchUserIdsHelperInterface] = twitchUserIdsHelper

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!addglobaltriviacontroller\b', re.IGNORECASE),
        })

        self.__argumentsPattern: Final[Pattern] = re.compile(r'^\s*!\w+\s+@?(\w+)', re.IGNORECASE)

    @property
    def commandName(self) -> str:
        return 'AddGlobalTriviaControllerChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not await self.__hasPermissions(chatMessage):
            return ChatCommandResult.IGNORED

        arguments = await self.__parseArguments(
            chatMessage = chatMessage,
        )

        if arguments is None:
            self.__twitchChatMessenger.send(
                text = f'⚠ Invalid arguments! Example use: !addglobaltriviacontroller @{chatMessage.chatterUserLogin}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Invalid arguments ({arguments=}) ({chatMessage=})')
            return ChatCommandResult.CONSUMED

        try:
            result = await self.__triviaGameControllersHelper.addGlobalController(
                userId = arguments.chatterUserId,
            )
        except TriviaGameControllerAlreadyExistsException as e:
            self.__timber.log(self.commandName, f'Failed to add global trivia controller as they\'ve already been added ({arguments=}) ({chatMessage=})', e, traceback.format_exc())

            self.__twitchChatMessenger.send(
                text = f'⚠ Failed to add @{arguments.chatterUserName} as a global trivia controller as they\'ve already been added',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            return ChatCommandResult.CONSUMED

        self.__twitchChatMessenger.send(
            text = f'ⓘ Added @{result.userName} as a global trivia controller. There are now {result.newTotal} global trivia controller(s)',
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )

        self.__timber.log(self.commandName, f'Consumed ({result=}) ({arguments=}) ({chatMessage=})')
        return ChatCommandResult.CONSUMED

    async def __hasPermissions(self, chatMessage: TwitchChatMessage) -> bool:
        isAdministrator = chatMessage.chatterUserId == await self.__administratorProvider.getAdministratorUserId()

        return isAdministrator

    async def __parseArguments(self, chatMessage: TwitchChatMessage) -> Arguments | None:
        argumentsMatch = self.__argumentsPattern.match(chatMessage.text)
        if argumentsMatch is None:
            return None

        chatterUserName = argumentsMatch.group(1)

        try:
            chatterUserData = await self.__twitchUserIdsHelper.requireByLoginOrName(
                userLoginOrName = chatterUserName,
                twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
                    twitchChannelId = chatMessage.twitchChannelId,
                ),
            )
        except Exception as e:
            self.__timber.log(self.commandName, f'Failed to fetch user data for the given chatter username ({chatterUserName=}) ({argumentsMatch=}) ({chatMessage=})', e, traceback.format_exc())
            return None

        return AddGlobalTriviaControllerChatCommand.Arguments(
            chatterUserId = chatterUserData.userId,
            chatterUserLogin = chatterUserData.userLogin,
            chatterUserName = chatterUserData.userName,
        )
