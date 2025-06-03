from typing import Final

from .absChatCommand import AbsChatCommand
from ..misc import utils as utils
from ..misc.generalSettingsRepository import GeneralSettingsRepository
from ..timber.timberInterface import TimberInterface
from ..trivia.actions.checkAnswerTriviaAction import CheckAnswerTriviaAction
from ..trivia.triviaGameMachineInterface import TriviaGameMachineInterface
from ..trivia.triviaIdGeneratorInterface import TriviaIdGeneratorInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class AnswerChatCommand(AbsChatCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        triviaGameMachine: TriviaGameMachineInterface,
        triviaIdGenerator: TriviaIdGeneratorInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise TypeError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameMachine, TriviaGameMachineInterface):
            raise TypeError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')
        elif not isinstance(triviaIdGenerator, TriviaIdGeneratorInterface):
            raise TypeError(f'triviaIdGenerator argument is malformed: \"{triviaIdGenerator}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__generalSettingsRepository: Final[GeneralSettingsRepository] = generalSettingsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__triviaGameMachine: Final[TriviaGameMachineInterface] = triviaGameMachine
        self.__triviaIdGenerator: Final[TriviaIdGeneratorInterface] = triviaIdGenerator
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled:
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            return

        actionId = await self.__triviaIdGenerator.generateActionId()
        answer = ' '.join(splits[1:])

        self.__triviaGameMachine.submitAction(CheckAnswerTriviaAction(
            actionId = actionId,
            answer = answer,
            twitchChannel = user.handle,
            twitchChannelId = await ctx.getTwitchChannelId(),
            twitchChatMessageId = await ctx.getMessageId(),
            userId = ctx.getAuthorId(),
            userName = ctx.getAuthorName()
        ))

        self.__timber.log('AnswerChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} ({actionId=})')
