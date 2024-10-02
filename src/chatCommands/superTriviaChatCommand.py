import traceback

from .absChatCommand import AbsChatCommand
from ..misc import utils as utils
from ..misc.generalSettingsRepository import GeneralSettingsRepository
from ..timber.timberInterface import TimberInterface
from ..trivia.builder.triviaGameBuilderInterface import TriviaGameBuilderInterface
from ..trivia.questions.triviaSource import TriviaSource
from ..trivia.triviaGameMachineInterface import TriviaGameMachineInterface
from ..trivia.triviaSettingsRepositoryInterface import TriviaSettingsRepositoryInterface
from ..trivia.triviaUtilsInterface import TriviaUtilsInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface
from ..twitch.timeout.twitchTimeoutHelperInterface import TwitchTimeoutHelperInterface
from ..twitch.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..twitch.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.userInterface import UserInterface
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
        twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface | None,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTimeoutHelper: TwitchTimeoutHelperInterface | None,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
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
        elif twitchFriendsUserIdRepository is not None and not isinstance(twitchFriendsUserIdRepository, TwitchFriendsUserIdRepositoryInterface):
            raise TypeError(f'twitchFriendsUserIdRepository argument is malformed: \"{twitchFriendsUserIdRepository}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif twitchTimeoutHelper is not None and not isinstance(twitchTimeoutHelper, TwitchTimeoutHelperInterface):
            raise TypeError(f'twitchTimeoutHelper argument is malformed: \"{twitchTimeoutHelper}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
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
        self.__twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface | None = twitchFriendsUserIdRepository
        self.__twitchHandleProvider: TwitchHandleProviderInterface = twitchHandleProvider
        self.__twitchTimeoutHelper: TwitchTimeoutHelperInterface | None = twitchTimeoutHelper
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
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
                await self.__twitchUtils.safeSend(
                    messageable = ctx,
                    message = f'⚠ Error converting the given count into an int. Example: !supertrivia 2',
                    replyMessageId = await ctx.getMessageId()
                )
                return

            maxNumberOfGames = await self.__triviaSettingsRepository.getMaxSuperTriviaGameQueueSize()

            if numberOfGames < 1 or numberOfGames > maxNumberOfGames:
                self.__timber.log('SuperTriviaChatCommand', f'The numberOfGames argument given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} is out of bounds ({numberOfGames}) (converted from \"{numberOfGamesStr}\")')
                await self.__twitchUtils.safeSend(
                    messageable = ctx,
                    message = f'⚠ The given count is an unexpected number, please try again. Example: !supertrivia 2',
                    replyMessageId = await ctx.getMessageId()
                )
                return

        triviaSource: TriviaSource | None = None

        match splits[0]:
            case '!supertrivialotr':
                triviaSource = TriviaSource.LORD_OF_THE_RINGS

        if await self.__scamStashio(
            triviaSource = triviaSource,
            ctx = ctx,
            user = user
        ):
            self.__timber.log('SuperTriviaChatCommand', f'Handled {splits[0]} command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
            return

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

    async def __scamStashio(
        self,
        triviaSource: TriviaSource | None,
        ctx: TwitchContext,
        user: UserInterface
    ) -> bool:
        if triviaSource is not TriviaSource.LORD_OF_THE_RINGS:
            return False
        elif not user.isSuperTriviaLotrTimeoutEnabled:
            return False

        twitchFriendsUserIdRepository = self.__twitchFriendsUserIdRepository
        twitchTimeoutHelper = self.__twitchTimeoutHelper

        if twitchFriendsUserIdRepository is None or twitchTimeoutHelper is None:
            return False
        elif ctx.getAuthorId() != await twitchFriendsUserIdRepository.getStashiocatUserId():
            return False

        twitchAccessToken = await self.__twitchTokensRepository.getAccessToken(
            twitchChannel = await self.__twitchHandleProvider.getTwitchHandle()
        )

        twitchChannelAccessToken = await self.__twitchTokensRepository.getAccessTokenById(
            twitchChannelId = await ctx.getTwitchChannelId()
        )

        if not utils.isValidStr(twitchAccessToken) or not utils.isValidStr(twitchChannelAccessToken):
            return False

        await twitchTimeoutHelper.timeout(
            durationSeconds = 600,
            reason = f'{ctx.getAuthorName()} is scamming via the !supertrivialotr command',
            twitchAccessToken = twitchAccessToken,
            twitchChannelAccessToken = twitchChannelAccessToken,
            twitchChannelId = await ctx.getTwitchChannelId(),
            userIdToTimeout = ctx.getAuthorId(),
            user = user
        )

        message = f'Wow @{ctx.getAuthorName()} is scamming with this command again 😡'

        while len(message) < self.__twitchUtils.maxMessageSize - len(' RIPBOZO'):
            message = f'{message}' + ' RIPBOZO'

        await self.__twitchUtils.safeSend(messageable = ctx, message = message.strip())
        return True
