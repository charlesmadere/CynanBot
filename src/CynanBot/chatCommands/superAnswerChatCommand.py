import CynanBot.misc.utils as utils
from CynanBot.chatCommands.absChatCommand import AbsChatCommand
from CynanBot.generalSettingsRepository import GeneralSettingsRepository
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.actions.checkSuperAnswerTriviaAction import \
    CheckSuperAnswerTriviaAction
from CynanBot.trivia.triviaGameMachineInterface import \
    TriviaGameMachineInterface
from CynanBot.trivia.triviaIdGeneratorInterface import \
    TriviaIdGeneratorInterface
from CynanBot.twitch.configuration.twitchContext import TwitchContext
from CynanBot.users.usersRepositoryInterface import UsersRepositoryInterface


class SuperAnswerChatCommand(AbsChatCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        triviaGameMachine: TriviaGameMachineInterface,
        triviaIdGenerator: TriviaIdGeneratorInterface,
        usersRepository: UsersRepositoryInterface
    ):
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(triviaGameMachine, TriviaGameMachineInterface), f"malformed {triviaGameMachine=}"
        assert isinstance(triviaIdGenerator, TriviaIdGeneratorInterface), f"malformed {triviaIdGenerator=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__triviaGameMachine: TriviaGameMachineInterface = triviaGameMachine
        self.__triviaIdGenerator: TriviaIdGeneratorInterface = triviaIdGenerator
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isTriviaGameEnabled() or not generalSettings.isSuperTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled() or not user.isSuperTriviaGameEnabled():
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            return

        answer = ' '.join(splits[1:])

        self.__triviaGameMachine.submitAction(CheckSuperAnswerTriviaAction(
            actionId = await self.__triviaIdGenerator.generateActionId(),
            answer = answer,
            twitchChannel = user.getHandle(),
            userId = ctx.getAuthorId(),
            userName = ctx.getAuthorName()
        ))

        self.__timber.log('SuperAnswerCommand', f'Handled !superanswer command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
