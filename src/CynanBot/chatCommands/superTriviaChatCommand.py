import traceback

import CynanBot.misc.utils as utils
from CynanBot.chatCommands.absChatCommand import AbsChatCommand
from CynanBot.generalSettingsRepository import GeneralSettingsRepository
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.builder.triviaGameBuilderInterface import \
    TriviaGameBuilderInterface
from CynanBot.trivia.triviaGameMachineInterface import \
    TriviaGameMachineInterface
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface
from CynanBot.trivia.triviaUtilsInterface import TriviaUtilsInterface
from CynanBot.twitch.configuration.twitchContext import TwitchContext
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.users.usersRepositoryInterface import UsersRepositoryInterface
from CynanBot.trivia.questions.triviaSource import TriviaSource

class SuperTriviaChatCommand(AbsChatCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        triviaGameBuilder: TriviaGameBuilderInterface,
        triviaGameMachine: TriviaGameMachineInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
        triviaUtils: TriviaUtilsInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise TypeError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameBuilder, TriviaGameBuilderInterface):
            raise TypeError(f'triviaGameBuilder argument is malformed: \"{triviaGameBuilder}\"')
        elif not isinstance(triviaGameMachine, TriviaGameMachineInterface):
            raise TypeError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')
        elif not isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface):
            raise TypeError(f'triviaSettingsRepository argument is malformed: \"{triviaSettingsRepository}\"')
        elif not isinstance(triviaUtils, TriviaUtilsInterface):
            raise TypeError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__triviaGameBuilder: TriviaGameBuilderInterface = triviaGameBuilder
        self.__triviaGameMachine: TriviaGameMachineInterface = triviaGameMachine
        self.__triviaSettingsRepository: TriviaSettingsRepositoryInterface = triviaSettingsRepository
        self.__triviaUtils: TriviaUtilsInterface = triviaUtils
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isTriviaGameEnabled() or not generalSettings.isSuperTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled() or not user.isSuperTriviaGameEnabled():
            return

        # For the time being, this command is intentionally not checking for mod status, as it has
        # been determined that super trivia game controllers shouldn't necessarily have to be mod.

        if not await self.__triviaUtils.isPrivilegedTriviaUser(
            twitchChannel = user.getHandle(),
            twitchChannelId = await ctx.getTwitchChannelId(),
            userId = ctx.getAuthorId()
        ):
            return

        numberOfGames = 1
        splits = utils.getCleanedSplits(ctx.getMessageContent())

        if len(splits) >= 2:
            numberOfGamesStr = splits[1]

            try:
                numberOfGames = int(numberOfGamesStr)
            except (SyntaxError, TypeError, ValueError) as e:
                self.__timber.log('SuperTriviaChatCommand', f'Unable to convert the numberOfGamesStr ({numberOfGamesStr}) argument into an int (given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}): {e}', e, traceback.format_exc())
                await self.__twitchUtils.safeSend(ctx, f'⚠ Error converting the given count into an int. Example: !supertrivia 2')
                return

            maxNumberOfGames = await self.__triviaSettingsRepository.getMaxSuperTriviaGameQueueSize()

            if numberOfGames < 1 or numberOfGames > maxNumberOfGames:
                self.__timber.log('SuperTriviaChatCommand', f'The numberOfGames argument given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} is out of bounds ({numberOfGames}) (converted from \"{numberOfGamesStr}\")')
                await self.__twitchUtils.safeSend(ctx, f'⚠ The given count is an unexpected number, please try again. Example: !supertrivia 2')
                return

      # match splits[0]:
      #     case '!supertrivialotr':
      #         s
      #     case _:

        triviaSource = None

        match splits[0]:
            case '!supertrivialotr':
                triviaSource = TriviaSource.LORD_OF_THE_RINGS
                
        startNewSuperTriviaGameAction = await self.__triviaGameBuilder.createNewSuperTriviaGame(
            twitchChannel = user.getHandle(),
            twitchChannelId = await ctx.getTwitchChannelId(),
            numberOfGames = numberOfGames,
            requiredTriviaSource = triviaSource
        )

        if startNewSuperTriviaGameAction is None:
            return

        self.__triviaGameMachine.submitAction(startNewSuperTriviaGameAction)
        
        # Presumably, a command should always be the first item in the splits array, use this ref
        # just in case we want to add more specified supertrivia commands in the future.

        self.__timber.log('SuperTriviaChatCommand', f'Handled {splits[0]} command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
