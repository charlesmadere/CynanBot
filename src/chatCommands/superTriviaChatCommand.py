import re
import traceback
from typing import Collection, Final, Pattern

from .absChatCommand import AbsChatCommand
from .chatCommandResult import ChatCommandResult
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..trivia.builder.triviaGameBuilderInterface import TriviaGameBuilderInterface
from ..trivia.gameController.triviaGameControllersHelperInterface import TriviaGameControllersHelperInterface
from ..trivia.questions.triviaSource import TriviaSource
from ..trivia.settings.triviaSettingsInterface import TriviaSettingsInterface
from ..trivia.triviaGameMachineInterface import TriviaGameMachineInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class SuperTriviaChatCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        timber: TimberInterface,
        triviaGameBuilder: TriviaGameBuilderInterface,
        triviaGameControllersHelper: TriviaGameControllersHelperInterface,
        triviaGameMachine: TriviaGameMachineInterface,
        triviaSettings: TriviaSettingsInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameBuilder, TriviaGameBuilderInterface):
            raise TypeError(f'triviaGameBuilder argument is malformed: \"{triviaGameBuilder}\"')
        elif not isinstance(triviaGameControllersHelper, TriviaGameControllersHelperInterface):
            raise TypeError(f'triviaGameControllersHelper argument is malformed: \"{triviaGameControllersHelper}\"')
        elif not isinstance(triviaGameMachine, TriviaGameMachineInterface):
            raise TypeError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')
        elif not isinstance(triviaSettings, TriviaSettingsInterface):
            raise TypeError(f'triviaSettings argument is malformed: \"{triviaSettings}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__timber: Final[TimberInterface] = timber
        self.__triviaGameBuilder: Final[TriviaGameBuilderInterface] = triviaGameBuilder
        self.__triviaGameControllersHelper: Final[TriviaGameControllersHelperInterface] = triviaGameControllersHelper
        self.__triviaGameMachine: Final[TriviaGameMachineInterface] = triviaGameMachine
        self.__triviaSettings: Final[TriviaSettingsInterface] = triviaSettings
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!supertrivias?\b', re.IGNORECASE),
            re.compile(r'^\s*!supertrivias?(?:lotr)?\b', re.IGNORECASE),
        })

        self.__lotrTriviaSourcePattern: Final[Pattern] = re.compile(r'^\s*!supertrivias?lotr\b', re.IGNORECASE)

    @property
    def commandName(self) -> str:
        return 'SuperTriviaChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not await self.__triviaSettings.isEnabled():
            return ChatCommandResult.IGNORED
        elif not chatMessage.twitchUser.isSuperTriviaGameEnabled:
            return ChatCommandResult.IGNORED
        elif not await self.__hasPermissions(chatMessage):
            return ChatCommandResult.IGNORED

        splits = utils.getCleanedSplits(chatMessage.text)
        numberOfGames = 1

        if len(splits) >= 2:
            numberOfGamesStr = splits[1]

            try:
                numberOfGames = int(numberOfGamesStr)
            except Exception as e:
                self.__twitchChatMessenger.send(
                    text = f'⚠ Error converting the given count into an int. Example: !supertrivia 2',
                    twitchChannelId = chatMessage.twitchChannelId,
                    replyMessageId = chatMessage.twitchChatMessageId,
                )

                self.__timber.log(self.commandName, f'Unable to convert the numberOfGamesStr argument into an int ({numberOfGames=}) ({numberOfGamesStr=}) ({splits=}) ({chatMessage=})', e, traceback.format_exc())
                return ChatCommandResult.CONSUMED

            maxNumberOfGames = await self.__triviaSettings.getMaxSuperTriviaGameQueueSize()

            if numberOfGames < 1 or numberOfGames > maxNumberOfGames:
                self.__twitchChatMessenger.send(
                    text = f'⚠ The given count is an unexpected number, please try again. Example: !supertrivia 2',
                    twitchChannelId = chatMessage.twitchChannelId,
                    replyMessageId = chatMessage.twitchChatMessageId,
                )

                self.__timber.log(self.commandName, f'The numberOfGames argument is out of bounds ({numberOfGames=}) ({numberOfGamesStr=}) ({splits=}) ({chatMessage=})')
                return ChatCommandResult.CONSUMED

        triviaSource: TriviaSource | None = None

        if self.__lotrTriviaSourcePattern.match(splits[0]):
            triviaSource = TriviaSource.LORD_OF_THE_RINGS

        action = await self.__triviaGameBuilder.createNewSuperTriviaGame(
            twitchChannelId = chatMessage.twitchChannelId,
            twitchUser = chatMessage.twitchUser,
            numberOfGames = numberOfGames,
            requiredTriviaSource = triviaSource,
        )

        if action is not None:
            self.__triviaGameMachine.submitAction(action)

        self.__timber.log(self.commandName, f'Consumed ({action=}) ({triviaSource=}) ({numberOfGames=}) ({splits=}) ({chatMessage=})')
        return ChatCommandResult.CONSUMED

    async def __hasPermissions(self, chatMessage: TwitchChatMessage) -> bool:
        isStreamer = chatMessage.chatterUserId == chatMessage.twitchChannelId

        isAdministrator = chatMessage.chatterUserId == await self.__administratorProvider.getAdministratorUserId()

        isPrivilegedTriviaUser = await self.__triviaGameControllersHelper.isController(
            twitchChannelId = chatMessage.twitchChannelId,
            userId = chatMessage.chatterUserId,
        )

        return isStreamer or isAdministrator or isPrivilegedTriviaUser
