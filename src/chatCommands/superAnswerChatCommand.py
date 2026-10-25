import re
from typing import Collection, Final, Pattern

from .absChatCommand import AbsChatCommand
from .chatCommandResult import ChatCommandResult
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..trivia.actions.checkSuperAnswerTriviaAction import CheckSuperAnswerTriviaAction
from ..trivia.settings.triviaSettingsInterface import TriviaSettingsInterface
from ..trivia.triviaGameMachineInterface import TriviaGameMachineInterface
from ..trivia.triviaIdGeneratorInterface import TriviaIdGeneratorInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class SuperAnswerChatCommand(AbsChatCommand):

    def __init__(
        self,
        timber: TimberInterface,
        triviaGameMachine: TriviaGameMachineInterface,
        triviaIdGenerator: TriviaIdGeneratorInterface,
        triviaSettings: TriviaSettingsInterface,
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameMachine, TriviaGameMachineInterface):
            raise TypeError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')
        elif not isinstance(triviaIdGenerator, TriviaIdGeneratorInterface):
            raise TypeError(f'triviaIdGenerator argument is malformed: \"{triviaIdGenerator}\"')
        elif not isinstance(triviaSettings, TriviaSettingsInterface):
            raise TypeError(f'triviaSettings argument is malformed: \"{triviaSettings}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__triviaGameMachine: Final[TriviaGameMachineInterface] = triviaGameMachine
        self.__triviaIdGenerator: Final[TriviaIdGeneratorInterface] = triviaIdGenerator
        self.__triviaSettings: Final[TriviaSettingsInterface] = triviaSettings

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!s(?:uper)?a(?:nswer)?\b', re.IGNORECASE),
            re.compile(r'^\s*!s(?:uper)?ta?\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'SuperAnswerChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not await self.__triviaSettings.isEnabled():
            return ChatCommandResult.IGNORED
        elif not chatMessage.twitchUser.isSuperTriviaGameEnabled:
            return ChatCommandResult.IGNORED

        splits = utils.getCleanedSplits(chatMessage.text)
        if len(splits) < 2:
            return ChatCommandResult.IGNORED

        actionId = await self.__triviaIdGenerator.generateActionId()
        answer = ' '.join(splits[1:])

        self.__triviaGameMachine.submitAction(CheckSuperAnswerTriviaAction(
            actionId = actionId,
            answer = answer,
            twitchChannel = chatMessage.twitchChannel,
            twitchChannelId = chatMessage.twitchChannelId,
            twitchChatMessageId = chatMessage.twitchChatMessageId,
            userId = chatMessage.chatterUserId,
            userLogin = chatMessage.chatterUserLogin,
            userName = chatMessage.chatterUserName,
        ))

        self.__timber.log(self.commandName, f'Consumed ({actionId=}) ({answer=}) ({chatMessage=})')
        return ChatCommandResult.CONSUMED
