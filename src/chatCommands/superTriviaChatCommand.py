import re
import traceback
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..misc import utils as utils
from ..misc.generalSettingsRepository import GeneralSettingsRepository
from ..timber.timberInterface import TimberInterface
from ..trivia.builder.triviaGameBuilderInterface import TriviaGameBuilderInterface
from ..trivia.questions.triviaSource import TriviaSource
from ..trivia.settings.triviaSettingsInterface import TriviaSettingsInterface
from ..trivia.triviaGameMachineInterface import TriviaGameMachineInterface
from ..trivia.triviaUtilsInterface import TriviaUtilsInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class SuperTriviaChatCommand(AbsChatCommand2):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        triviaGameBuilder: TriviaGameBuilderInterface,
        triviaGameMachine: TriviaGameMachineInterface,
        triviaSettings: TriviaSettingsInterface,
        triviaUtils: TriviaUtilsInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise TypeError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameBuilder, TriviaGameBuilderInterface):
            raise TypeError(f'triviaGameBuilder argument is malformed: \"{triviaGameBuilder}\"')
        elif not isinstance(triviaGameMachine, TriviaGameMachineInterface):
            raise TypeError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')
        elif not isinstance(triviaSettings, TriviaSettingsInterface):
            raise TypeError(f'triviaSettings argument is malformed: \"{triviaSettings}\"')
        elif not isinstance(triviaUtils, TriviaUtilsInterface):
            raise TypeError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__generalSettingsRepository: Final[GeneralSettingsRepository] = generalSettingsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__triviaGameBuilder: Final[TriviaGameBuilderInterface] = triviaGameBuilder
        self.__triviaGameMachine: Final[TriviaGameMachineInterface] = triviaGameMachine
        self.__triviaSettings: Final[TriviaSettingsInterface] = triviaSettings
        self.__triviaUtils: Final[TriviaUtilsInterface] = triviaUtils
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!supertrivia\b', re.IGNORECASE),
            re.compile(r'^\s*!supertrivia(?:lotr)?\b', re.IGNORECASE),
        })

        self.__lotrTriviaSourcePattern: Final[Pattern] = re.compile(r'^\s*!supertrivialotr\b', re.IGNORECASE)

    @property
    def commandName(self) -> str:
        return 'SuperTriviaChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isTriviaGameEnabled or not chatMessage.twitchUser.isSuperTriviaGameEnabled:
            return ChatCommandResult.IGNORED

        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        if not generalSettings.isTriviaGameEnabled() or not generalSettings.isSuperTriviaGameEnabled():
            return ChatCommandResult.IGNORED
        elif not await self.__triviaUtils.isPrivilegedTriviaUser(
            twitchChannelId = chatMessage.twitchChannelId,
            userId = chatMessage.chatterUserId,
        ):
            return ChatCommandResult.IGNORED

        numberOfGames = 1
        splits = utils.getCleanedSplits(chatMessage.text)

        if len(splits) >= 2:
            numberOfGamesStr: str | None = splits[1]

            try:
                numberOfGames = int(numberOfGamesStr)
            except Exception as e:
                self.__twitchChatMessenger.send(
                    text = f'⚠ Error converting the given count into an int. Example: !supertrivia 2',
                    twitchChannelId = chatMessage.twitchChannelId,
                    replyMessageId = chatMessage.twitchChatMessageId,
                )

                self.__timber.log(self.commandName, f'Unable to convert the numberOfGamesStr argument into an int ({numberOfGames=}) ({numberOfGamesStr=}) ({splits=}) ({chatMessage=})', e, traceback.format_exc())
                return ChatCommandResult.HANDLED

            maxNumberOfGames = await self.__triviaSettings.getMaxSuperTriviaGameQueueSize()

            if numberOfGames < 1 or numberOfGames > maxNumberOfGames:
                self.__twitchChatMessenger.send(
                    text = f'⚠ The given count is an unexpected number, please try again. Example: !supertrivia 2',
                    twitchChannelId = chatMessage.twitchChannelId,
                    replyMessageId = chatMessage.twitchChatMessageId,
                )

                self.__timber.log(self.commandName, f'The numberOfGames argument is out of bounds ({numberOfGames=}) ({numberOfGamesStr=}) ({splits=}) ({chatMessage=})')
                return ChatCommandResult.HANDLED

        triviaSource: TriviaSource | None = None

        if self.__lotrTriviaSourcePattern.match(splits[0]):
            triviaSource = TriviaSource.LORD_OF_THE_RINGS

        if chatMessage.twitchUser.arePranksEnabled and await self.__stopForPrank(
            twitchChannelId = chatMessage.twitchChannelId,
            userId = chatMessage.chatterUserId,
            triviaSource = triviaSource,
        ):
            return ChatCommandResult.HANDLED

        action = await self.__triviaGameBuilder.createNewSuperTriviaGame(
            twitchChannel = chatMessage.twitchChannel,
            twitchChannelId = chatMessage.twitchChannelId,
            numberOfGames = numberOfGames,
            requiredTriviaSource = triviaSource,
        )

        if action is None:
            return ChatCommandResult.IGNORED

        self.__triviaGameMachine.submitAction(action)
        self.__timber.log(self.commandName, f'Handled ({numberOfGames=}) ({triviaSource=}) ({chatMessage=})')
        return ChatCommandResult.HANDLED

    async def __stopForPrank(
        self,
        twitchChannelId: str,
        userId: str,
        triviaSource: TriviaSource | None,
    ) -> bool:
        # TODO prank code goes here
        return False
