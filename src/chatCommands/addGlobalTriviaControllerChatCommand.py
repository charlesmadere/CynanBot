import re
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..trivia.gameController.addTriviaGameControllerResult import AddTriviaGameControllerResult
from ..trivia.gameController.triviaGameGlobalControllersRepositoryInterface import \
    TriviaGameGlobalControllersRepositoryInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.handleProvider.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage
from ..twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class AddGlobalTriviaControllerChatCommand(AbsChatCommand2):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        timber: TimberInterface,
        triviaGameGlobalControllersRepository: TriviaGameGlobalControllersRepositoryInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameGlobalControllersRepository, TriviaGameGlobalControllersRepositoryInterface):
            raise TypeError(f'triviaGameGlobalControllersRepository argument is malformed: \"{triviaGameGlobalControllersRepository}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__timber: Final[TimberInterface] = timber
        self.__triviaGameGlobalControllersRepository: Final[TriviaGameGlobalControllersRepositoryInterface] = triviaGameGlobalControllersRepository
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!addglobaltriviacontroller\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'AddGlobalTriviaControllerChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not await self.__hasPermissions(chatMessage):
            return ChatCommandResult.IGNORED

        twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()

        splits = utils.getCleanedSplits(chatMessage.text)
        if len(splits) < 2:
            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to add global trivia controller as no username argument was given. Example: !addglobaltriviacontroller @{twitchHandle}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Attempted to handle command, but no arguments were supplied ({splits=}) ({chatMessage=})')
            return ChatCommandResult.HANDLED

        targetUserName: str | None = utils.removePreceedingAt(splits[1])
        if not utils.isValidStr(targetUserName) or not utils.strContainsAlphanumericCharacters(targetUserName):
            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to add global trivia controller as username argument is malformed. Example: !addglobaltriviacontroller @{twitchHandle}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Attempted to handle command, but the username argument is malformed ({targetUserName=}) ({splits=}) ({chatMessage=})')
            return ChatCommandResult.HANDLED

        targetUserId = await self.__userIdsRepository.fetchUserId(
            userName = targetUserName,
            twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
                twitchChannelId = chatMessage.twitchChannelId,
            ),
        )

        if not utils.isValidStr(targetUserId):
            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to add global trivia controller as no user ID could be found for \"{targetUserName}\"',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Failed to fetch user ID for the given username argument ({targetUserId=}) ({targetUserName=}) ({splits=}) ({chatMessage=})')
            return ChatCommandResult.HANDLED

        result = await self.__triviaGameGlobalControllersRepository.addController(
            userId = targetUserId,
        )

        match result:
            case AddTriviaGameControllerResult.ADDED:
                self.__twitchChatMessenger.send(
                    text = f'ⓘ Added @{targetUserName} as a global trivia game controller',
                    twitchChannelId = chatMessage.twitchChannelId,
                    replyMessageId = chatMessage.twitchChatMessageId,
                )

            case AddTriviaGameControllerResult.ALREADY_EXISTS:
                self.__twitchChatMessenger.send(
                    text = f'⚠ Tried adding @{targetUserName} as a global trivia game controller, but they already were one',
                    twitchChannelId = chatMessage.twitchChannelId,
                    replyMessageId = chatMessage.twitchChatMessageId,
                )

            case AddTriviaGameControllerResult.ERROR:
                self.__twitchChatMessenger.send(
                    text = f'⚠ An error occurred when trying to add @{targetUserName} as a global trivia game controller!',
                    twitchChannelId = chatMessage.twitchChannelId,
                    replyMessageId = chatMessage.twitchChatMessageId,
                )

        self.__timber.log(self.commandName, f'Handled ({result=}) ({targetUserId=}) ({targetUserName=}) ({chatMessage=})')
        return ChatCommandResult.HANDLED

    async def __hasPermissions(self, chatMessage: TwitchChatMessage) -> bool:
        return chatMessage.chatterUserId == await self.__administratorProvider.getAdministratorUserId()
