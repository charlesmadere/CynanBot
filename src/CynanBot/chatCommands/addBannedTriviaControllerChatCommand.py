import CynanBot.misc.utils as utils
from CynanBot.administratorProviderInterface import \
    AdministratorProviderInterface
from CynanBot.chatCommands.absChatCommand import AbsChatCommand
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.banned.addBannedTriviaGameControllerResult import \
    AddBannedTriviaGameControllerResult
from CynanBot.trivia.banned.bannedTriviaGameControllersRepositoryInterface import \
    BannedTriviaGameControllersRepositoryInterface
from CynanBot.twitch.configuration.twitchContext import TwitchContext
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.users.usersRepositoryInterface import UsersRepositoryInterface


class AddBannedTriviaControllerChatCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        bannedTriviaGameControllersRepository: BannedTriviaGameControllersRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(bannedTriviaGameControllersRepository, BannedTriviaGameControllersRepositoryInterface):
            raise TypeError(f'bannedTriviaGameControllersRepository argument is malformed: \"{timber}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__bannedTriviaGameControllersRepository: BannedTriviaGameControllersRepositoryInterface = bannedTriviaGameControllersRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if ctx.getAuthorId() != administrator:
            self.__timber.log('AddBannedTriviaControllerChatCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('AddBannedTriviaControllerChatCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {ctx.getTwitchChannelName()}, but no arguments were supplied')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to add banned trivia controller as no username argument was given. Example: !addbannedtriviacontroller {administrator}')
            return

        userName = utils.removePreceedingAt(splits[1])
        if not utils.isValidStr(userName):
            self.__timber.log('AddBannedTriviaControllerChatCommand', f'Attempted to handle command for {userName}:{ctx.getAuthorId()} in {user.getHandle()}, but username argument is malformed: \"{userName}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to add banned trivia controller as username argument is malformed. Example: !addbannedtriviacontroller {user.getHandle()}')
            return

        result = await self.__bannedTriviaGameControllersRepository.addBannedController(
            userName = userName
        )

        if result is AddBannedTriviaGameControllerResult.ADDED:
            await self.__twitchUtils.safeSend(ctx, f'ⓘ Added {userName} as a banned trivia game controller.')
        elif result is AddBannedTriviaGameControllerResult.ALREADY_EXISTS:
            await self.__twitchUtils.safeSend(ctx, f'ⓘ Tried adding {userName} as a banned trivia game controller, but they already were one.')
        elif result is AddBannedTriviaGameControllerResult.ERROR:
            await self.__twitchUtils.safeSend(ctx, f'⚠ An error occurred when trying to add {userName} as a banned trivia game controller!')
        else:
            await self.__twitchUtils.safeSend(ctx, f'⚠ An unknown error occurred when trying to add {userName} as a banned trivia game controller!')
            self.__timber.log('AddBannedTriviaControllerChatCommand', f'Encountered unknown AddBannedTriviaGameControllerResult value ({result}) when trying to add \"{userName}\" as a banned trivia game controller for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
            raise RuntimeError(f'Encountered unknown AddBannedTriviaGameControllerResult value ({result}) when trying to add \"{userName}\" as a banned trivia game controller for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')

        self.__timber.log('AddBannedTriviaControllerChatCommand', f'Handled !addbannedtriviacontroller command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {ctx.getTwitchChannelName()}')
