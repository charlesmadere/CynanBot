import re
from typing import Collection, Final, Pattern

from .absChatCommand import AbsChatCommand
from .chatCommandResult import ChatCommandResult
from ..timber.timberInterface import TimberInterface
from ..trivia.actions.clearSuperTriviaQueueTriviaAction import ClearSuperTriviaQueueTriviaAction
from ..trivia.gameController.triviaGameControllersHelperInterface import TriviaGameControllersHelperInterface
from ..trivia.settings.triviaSettingsInterface import TriviaSettingsInterface
from ..trivia.triviaGameMachineInterface import TriviaGameMachineInterface
from ..trivia.triviaIdGeneratorInterface import TriviaIdGeneratorInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class ClearSuperTriviaQueueChatCommand(AbsChatCommand):

    def __init__(
        self,
        timber: TimberInterface,
        triviaGameControllersHelper: TriviaGameControllersHelperInterface,
        triviaGameMachine: TriviaGameMachineInterface,
        triviaIdGenerator: TriviaIdGeneratorInterface,
        triviaSettings: TriviaSettingsInterface,
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameControllersHelper, TriviaGameControllersHelperInterface):
            raise TypeError(f'triviaGameControllersHelper ')
        elif not isinstance(triviaGameMachine, TriviaGameMachineInterface):
            raise TypeError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')
        elif not isinstance(triviaIdGenerator, TriviaIdGeneratorInterface):
            raise TypeError(f'triviaIdGenerator argument is malformed: \"{triviaIdGenerator}\"')
        elif not isinstance(triviaSettings, TriviaSettingsInterface):
            raise TypeError(f'triviaSettings argument is malformed: \"{triviaSettings}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__triviaGameControllersHelper: Final[TriviaGameControllersHelperInterface] = triviaGameControllersHelper
        self.__triviaGameMachine: Final[TriviaGameMachineInterface] = triviaGameMachine
        self.__triviaIdGenerator: Final[TriviaIdGeneratorInterface] = triviaIdGenerator
        self.__triviaSettings: Final[TriviaSettingsInterface] = triviaSettings

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!clear(?:super)?trivias?\b', re.IGNORECASE),
            re.compile(r'^\s*!clear(?:super)?trivias?queue\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'ClearSuperTriviaQueueChatCommand'

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

        actionId = await self.__triviaIdGenerator.generateActionId()

        self.__triviaGameMachine.submitAction(ClearSuperTriviaQueueTriviaAction(
            actionId = actionId,
            twitchChannel = chatMessage.twitchChannel,
            twitchChannelId = chatMessage.twitchChannelId,
            twitchChatMessageId = chatMessage.twitchChatMessageId,
        ))

        self.__timber.log(self.commandName, f'Consumed ({actionId=}) ({chatMessage=})')
        return ChatCommandResult.CONSUMED

    async def __hasPermissions(self, chatMessage: TwitchChatMessage) -> bool:
        isStreamer = chatMessage.chatterUserId == chatMessage.twitchChannelId

        isTriviaController = await self.__triviaGameControllersHelper.isController(
            twitchChannelId = chatMessage.twitchChannelId,
            userId = chatMessage.chatterUserId,
        )

        return isStreamer or isTriviaController
