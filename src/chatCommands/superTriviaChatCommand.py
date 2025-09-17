import traceback
from typing import Final

from .absChatCommand import AbsChatCommand
from ..misc import utils as utils
from ..misc.generalSettingsRepository import GeneralSettingsRepository
from ..timber.timberInterface import TimberInterface
from ..trivia.builder.triviaGameBuilderInterface import TriviaGameBuilderInterface
from ..trivia.questions.triviaSource import TriviaSource
from ..trivia.settings.triviaSettingsRepositoryInterface import TriviaSettingsRepositoryInterface
from ..trivia.triviaGameMachineInterface import TriviaGameMachineInterface
from ..trivia.triviaUtilsInterface import TriviaUtilsInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class SuperTriviaChatCommand(AbsChatCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        triviaGameBuilder: TriviaGameBuilderInterface,
        triviaGameMachine: TriviaGameMachineInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
        triviaUtils: TriviaUtilsInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        usersRepository: UsersRepositoryInterface,
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
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__generalSettingsRepository: Final[GeneralSettingsRepository] = generalSettingsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__triviaGameBuilder: Final[TriviaGameBuilderInterface] = triviaGameBuilder
        self.__triviaGameMachine: Final[TriviaGameMachineInterface] = triviaGameMachine
        self.__triviaSettingsRepository: Final[TriviaSettingsRepositoryInterface] = triviaSettingsRepository
        self.__triviaUtils: Final[TriviaUtilsInterface] = triviaUtils
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        # For the time being, this command is intentionally not checking for mod status, as it has
        # been determined that super trivia game controllers shouldn't necessarily have to be mod.
        if not generalSettings.isTriviaGameEnabled() or not generalSettings.isSuperTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled or not user.isSuperTriviaGameEnabled:
            return
        elif not await self.__triviaUtils.isPrivilegedTriviaUser(
            twitchChannelId = await ctx.getTwitchChannelId(),
            userId = ctx.getAuthorId(),
        ):
            return

        numberOfGames = 1
        splits = utils.getCleanedSplits(ctx.getMessageContent())

        if len(splits) >= 2:
            numberOfGamesStr = splits[1]

            try:
                numberOfGames = int(numberOfGamesStr)
            except Exception as e:
                self.__timber.log('SuperTriviaChatCommand', f'Unable to convert the numberOfGamesStr argument into an int (given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}) ({numberOfGamesStr=}): {e}', e, traceback.format_exc())
                self.__twitchChatMessenger.send(
                    text = f'⚠ Error converting the given count into an int. Example: !supertrivia 2',
                    twitchChannelId = await ctx.getTwitchChannelId(),
                    replyMessageId = await ctx.getMessageId(),
                )
                return

            maxNumberOfGames = await self.__triviaSettingsRepository.getMaxSuperTriviaGameQueueSize()

            if numberOfGames < 1 or numberOfGames > maxNumberOfGames:
                self.__timber.log('SuperTriviaChatCommand', f'The numberOfGames argument given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} is out of bounds ({numberOfGames=}) ({numberOfGamesStr=})')
                self.__twitchChatMessenger.send(
                    text = f'⚠ The given count is an unexpected number, please try again. Example: !supertrivia 2',
                    twitchChannelId = await ctx.getTwitchChannelId(),
                    replyMessageId = await ctx.getMessageId(),
                )
                return

        triviaSource: TriviaSource | None = None

        match splits[0]:
            case '!supertrivialotr':
                triviaSource = TriviaSource.LORD_OF_THE_RINGS

        if user.arePranksEnabled and await self.__stopForPrank(
            twitchChannelId = await ctx.getTwitchChannelId(),
            userId = ctx.getAuthorId(),
            triviaSource = triviaSource,
        ):
            return

        action = await self.__triviaGameBuilder.createNewSuperTriviaGame(
            twitchChannel = user.handle,
            twitchChannelId = await ctx.getTwitchChannelId(),
            numberOfGames = numberOfGames,
            requiredTriviaSource = triviaSource,
        )

        if action is None:
            return

        self.__triviaGameMachine.submitAction(action)
        self.__timber.log('SuperTriviaChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} ({numberOfGames=}) ({triviaSource=})')

    async def __stopForPrank(
        self,
        twitchChannelId: str,
        userId: str,
        triviaSource: TriviaSource | None,
    ) -> bool:
        if triviaSource is not TriviaSource.LORD_OF_THE_RINGS:
            return False

        # TODO prank code goes here
        return False
