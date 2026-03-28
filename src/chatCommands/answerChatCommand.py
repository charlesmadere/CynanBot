import re
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..misc import utils as utils
from ..misc.generalSettingsRepository import GeneralSettingsRepository
from ..timber.timberInterface import TimberInterface
from ..trivia.actions.checkAnswerTriviaAction import CheckAnswerTriviaAction
from ..trivia.triviaGameMachineInterface import TriviaGameMachineInterface
from ..trivia.triviaIdGeneratorInterface import TriviaIdGeneratorInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class AnswerChatCommand(AbsChatCommand2):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        triviaGameMachine: TriviaGameMachineInterface,
        triviaIdGenerator: TriviaIdGeneratorInterface,
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise TypeError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameMachine, TriviaGameMachineInterface):
            raise TypeError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')
        elif not isinstance(triviaIdGenerator, TriviaIdGeneratorInterface):
            raise TypeError(f'triviaIdGenerator argument is malformed: \"{triviaIdGenerator}\"')

        self.__generalSettingsRepository: Final[GeneralSettingsRepository] = generalSettingsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__triviaGameMachine: Final[TriviaGameMachineInterface] = triviaGameMachine
        self.__triviaIdGenerator: Final[TriviaIdGeneratorInterface] = triviaIdGenerator

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!a(?:nswer)?\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'AnswerChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isTriviaGameEnabled:
            return ChatCommandResult.IGNORED

        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        if not generalSettings.isTriviaGameEnabled():
            return ChatCommandResult.IGNORED

        splits = utils.getCleanedSplits(chatMessage.text)
        if len(splits) < 2:
            return ChatCommandResult.IGNORED

        actionId = await self.__triviaIdGenerator.generateActionId()
        answer = ' '.join(splits[1:])

        self.__triviaGameMachine.submitAction(CheckAnswerTriviaAction(
            actionId = actionId,
            answer = answer,
            twitchChannel = chatMessage.twitchChannel,
            twitchChannelId = chatMessage.twitchChannelId,
            twitchChatMessageId = chatMessage.twitchChatMessageId,
            userId = chatMessage.chatterUserId,
            userName = chatMessage.chatterUserName,
        ))

        self.__timber.log(self.commandName, f'Handled ({actionId=}) ({chatMessage=})')
        return ChatCommandResult.HANDLED
