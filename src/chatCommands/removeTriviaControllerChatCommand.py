import re
import traceback
from dataclasses import dataclass
from typing import Collection, Final, Pattern

from .absChatCommand import AbsChatCommand
from .chatCommandResult import ChatCommandResult
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..misc.generalSettingsRepository import GeneralSettingsRepository
from ..timber.timberInterface import TimberInterface
from ..trivia.gameController.removeTriviaGameControllerResult import RemoveTriviaGameControllerResult
from ..trivia.gameController.triviaGameControllersRepositoryInterface import TriviaGameControllersRepositoryInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage
from ..twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ..twitch.userIds.twitchUserIdsHelperInterface import TwitchUserIdsHelperInterface


class RemoveTriviaControllerChatCommand(AbsChatCommand):

    @dataclass(frozen = True, slots = True)
    class Arguments:
        chatterUserId: str
        chatterUserLogin: str
        chatterUserName: str

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        triviaGameControllersRepository: TriviaGameControllersRepositoryInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        twitchUserIdsHelper: TwitchUserIdsHelperInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise TypeError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameControllersRepository, TriviaGameControllersRepositoryInterface):
            raise TypeError(f'triviaGameControllersRepository argument is malformed: \"{triviaGameControllersRepository}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(twitchUserIdsHelper, TwitchUserIdsHelperInterface):
            raise TypeError(f'twitchUserIdsHelper argument is malformed: \"{twitchUserIdsHelper}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__generalSettingsRepository: Final[GeneralSettingsRepository] = generalSettingsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__triviaGameControllersRepository: Final[TriviaGameControllersRepositoryInterface] = triviaGameControllersRepository
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__twitchUserIdsHelper: Final[TwitchUserIdsHelperInterface] = twitchUserIdsHelper

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!del(?:ete)?triviacontroller\b', re.IGNORECASE),
            re.compile(r'^\s*!removetriviacontroller\b', re.IGNORECASE),
            re.compile(r'^\s*!rmtriviacontroller\b', re.IGNORECASE),
        })

        self.__argumentsPattern: Final[Pattern] = re.compile(r'^\s*!\w+\s+@?(\w+)', re.IGNORECASE)

    @property
    def commandName(self) -> str:
        return 'RemoveTriviaControllerChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isTriviaGameEnabled and not chatMessage.twitchUser.isSuperTriviaGameEnabled:
            return ChatCommandResult.IGNORED
        elif not await self.__hasPermissions(chatMessage):
            return ChatCommandResult.IGNORED

        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        if not generalSettings.isTriviaGameEnabled() and not generalSettings.isSuperTriviaGameEnabled():
            return ChatCommandResult.IGNORED

        arguments = await self.__parseArguments(
            chatMessage = chatMessage,
        )

        if arguments is None:
            self.__twitchChatMessenger.send(
                text = f'⚠ Invalid arguments! Example use: !removetriviacontroller @{chatMessage.chatterUserLogin}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Invalid arguments ({arguments=}) ({chatMessage=})')
            return ChatCommandResult.CONSUMED

        result = await self.__triviaGameControllersRepository.removeController(
            twitchChannelId = chatMessage.twitchChannelId,
            userId = arguments.chatterUserId,
        )

        match result:
            case RemoveTriviaGameControllerResult.DOES_NOT_EXIST:
                self.__twitchChatMessenger.send(
                    text = f'⚠ {arguments.chatterUserLogin} is not a trivia game controller',
                    twitchChannelId = chatMessage.twitchChannelId,
                    replyMessageId = chatMessage.twitchChatMessageId,
                )

            case RemoveTriviaGameControllerResult.ERROR:
                self.__twitchChatMessenger.send(
                    text = f'⚠ An error occurred when trying to remove {arguments.chatterUserLogin} as a trivia game controller!',
                    twitchChannelId = chatMessage.twitchChannelId,
                    replyMessageId = chatMessage.twitchChatMessageId,
                )

            case RemoveTriviaGameControllerResult.REMOVED:
                self.__twitchChatMessenger.send(
                    text = f'ⓘ Removed {arguments.chatterUserLogin} as a trivia game controller',
                    twitchChannelId = chatMessage.twitchChannelId,
                    replyMessageId = chatMessage.twitchChatMessageId,
                )

        self.__timber.log(self.commandName, f'Consumed ({result=}) ({arguments=}) ({chatMessage=})')
        return ChatCommandResult.CONSUMED

    async def __hasPermissions(self, chatMessage: TwitchChatMessage) -> bool:
        isStreamer = chatMessage.chatterUserId == chatMessage.twitchChannelId

        isAdministrator = chatMessage.chatterUserId == await self.__administratorProvider.getAdministratorUserId()

        return isStreamer or isAdministrator

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

        return RemoveTriviaControllerChatCommand.Arguments(
            chatterUserId = chatterUserData.userId,
            chatterUserLogin = chatterUserData.userLogin,
            chatterUserName = chatterUserData.userName,
        )
