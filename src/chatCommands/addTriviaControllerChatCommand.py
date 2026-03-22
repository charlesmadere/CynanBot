import re
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..misc.generalSettingsRepository import GeneralSettingsRepository
from ..timber.timberInterface import TimberInterface
from ..trivia.gameController.addTriviaGameControllerResult import AddTriviaGameControllerResult
from ..trivia.gameController.triviaGameControllersRepositoryInterface import TriviaGameControllersRepositoryInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.handleProvider.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage
from ..twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ..users.exceptions import NoSuchUserException
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class AddTriviaControllerChatCommand(AbsChatCommand2):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        triviaGameControllersRepository: TriviaGameControllersRepositoryInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
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
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__generalSettingsRepository: Final[GeneralSettingsRepository] = generalSettingsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__triviaGameControllersRepository: Final[TriviaGameControllersRepositoryInterface] = triviaGameControllersRepository
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!addtriviacontroller\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'AddTriviaControllerChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isTriviaGameEnabled and not chatMessage.twitchUser.isSuperTriviaGameEnabled:
            return ChatCommandResult.IGNORED
        elif chatMessage.chatterUserId != chatMessage.twitchChannelId and chatMessage.chatterUserId != await self.__administratorProvider.getAdministratorUserId():
            return ChatCommandResult.IGNORED

        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        if not generalSettings.isTriviaGameEnabled() and not generalSettings.isSuperTriviaGameEnabled():
            return ChatCommandResult.IGNORED

        twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()

        splits = utils.getCleanedSplits(chatMessage.text)
        if len(splits) < 2:
            self.__timber.log(self.commandName, f'Attempted to handle command, but no arguments were supplied ({splits=}) ({chatMessage=})')

            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to add trivia controller as no username argument was given. Example: !addtriviacontroller @{twitchHandle}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
            return ChatCommandResult.HANDLED

        targetUserName: str | None = utils.removePreceedingAt(splits[1])
        if not utils.isValidStr(targetUserName) or not utils.strContainsAlphanumericCharacters(targetUserName):
            self.__timber.log(self.commandName, f'Attempted to handle command, but username argument is malformed ({targetUserName=}) ({splits=}) ({chatMessage=})')

            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to add trivia controller as username argument is malformed. Example: !addtriviacontroller {twitchHandle}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
            return ChatCommandResult.HANDLED

        try:
            targetUserId = await self.__userIdsRepository.requireUserId(
                userName = targetUserName,
                twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
                    twitchChannelId = chatMessage.twitchChannelId,
                ),
            )
        except NoSuchUserException:
            self.__timber.log(self.commandName, f'Failed to fetch user ID for the given username argument ({targetUserName=}) ({splits=}) ({chatMessage=})')

            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to add trivia controller as no user ID could be found for the given username',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
            return ChatCommandResult.HANDLED

        result = await self.__triviaGameControllersRepository.addController(
            twitchChannelId = chatMessage.twitchChannelId,
            userId = targetUserId,
        )

        match result:
            case AddTriviaGameControllerResult.ADDED:
                self.__twitchChatMessenger.send(
                    text = f'ⓘ Added @{targetUserName} as a trivia game controller',
                    twitchChannelId = chatMessage.twitchChannelId,
                    replyMessageId = chatMessage.twitchChatMessageId,
                )

            case AddTriviaGameControllerResult.ALREADY_EXISTS:
                self.__twitchChatMessenger.send(
                    text = f'⚠ Tried adding @{targetUserName} as a trivia game controller, but they already were one',
                    twitchChannelId = chatMessage.twitchChannelId,
                    replyMessageId = chatMessage.twitchChatMessageId,
                )

            case AddTriviaGameControllerResult.ERROR:
                self.__twitchChatMessenger.send(
                    text = f'⚠ An error occurred when trying to add @{targetUserName} as a trivia game controller!',
                    twitchChannelId = chatMessage.twitchChannelId,
                    replyMessageId = chatMessage.twitchChatMessageId,
                )

        self.__timber.log(self.commandName, f'Handled ({result=}) ({targetUserId=}) ({targetUserName=})')
        return ChatCommandResult.HANDLED
