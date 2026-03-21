import re
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..trivia.banned.addBannedTriviaGameControllerResult import \
    AddBannedTriviaGameControllerResult
from ..trivia.banned.bannedTriviaGameControllersRepositoryInterface import \
    BannedTriviaGameControllersRepositoryInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.handleProvider.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage
from ..twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class AddBannedTriviaControllerChatCommand(AbsChatCommand2):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        bannedTriviaGameControllersRepository: BannedTriviaGameControllersRepositoryInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(bannedTriviaGameControllersRepository, BannedTriviaGameControllersRepositoryInterface):
            raise TypeError(f'bannedTriviaGameControllersRepository argument is malformed: \"{timber}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__bannedTriviaGameControllersRepository: Final[BannedTriviaGameControllersRepositoryInterface] = bannedTriviaGameControllersRepository
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!addbannedtriviacontroller\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'AddBannedTriviaControllerChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if chatMessage.chatterUserId != await self.__administratorProvider.getAdministratorUserId():
            return ChatCommandResult.IGNORED

        twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()

        splits = utils.getCleanedSplits(chatMessage.text)
        if len(splits) < 2:
            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to add banned trivia controller as no username argument was given. Example: !addbannedtriviacontroller @{twitchHandle}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
            self.__timber.log(self.commandName, f'Attempted to handle command, but no arguments were supplied ({splits=}) ({chatMessage=})')
            return ChatCommandResult.HANDLED

        targetUserName: str | None = utils.removePreceedingAt(splits[1])
        if not utils.isValidStr(targetUserName) or not utils.strContainsAlphanumericCharacters(targetUserName):
            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to add banned trivia controller as username argument is malformed. Example: !addbannedtriviacontroller @{twitchHandle}',
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
                text = f'⚠ Unable to add banned trivia controller as no user ID could be found for \"{targetUserName}\"',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Failed to fetch user ID for the given username argument ({targetUserId=}) ({targetUserName=}) ({splits=}) ({chatMessage=})')
            return ChatCommandResult.HANDLED

        result = await self.__bannedTriviaGameControllersRepository.addBannedController(
            userId = targetUserId,
        )

        match result:
            case AddBannedTriviaGameControllerResult.ADDED:
                self.__twitchChatMessenger.send(
                    text = f'ⓘ Added {targetUserName} as a banned trivia game controller',
                    twitchChannelId = chatMessage.twitchChannelId,
                    replyMessageId = chatMessage.twitchChatMessageId,
                )

            case AddBannedTriviaGameControllerResult.ALREADY_EXISTS:
                self.__twitchChatMessenger.send(
                    text = f'⚠ Tried adding {targetUserName} as a banned trivia game controller, but they already were one',
                    twitchChannelId = chatMessage.twitchChannelId,
                    replyMessageId = chatMessage.twitchChatMessageId,
                )

            case AddBannedTriviaGameControllerResult.ERROR:
                self.__twitchChatMessenger.send(
                    text = f'⚠ An error occurred when trying to add {targetUserName} as a banned trivia game controller!',
                    twitchChannelId = chatMessage.twitchChannelId,
                    replyMessageId = chatMessage.twitchChatMessageId,
                )

        self.__timber.log(self.commandName, f'Handled ({result=}) ({targetUserId=}) ({targetUserName})')
        return ChatCommandResult.HANDLED
