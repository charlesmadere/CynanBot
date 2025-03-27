from .absChatCommand import AbsChatCommand
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..trivia.banned.addBannedTriviaGameControllerResult import \
    AddBannedTriviaGameControllerResult
from ..trivia.banned.bannedTriviaGameControllersRepositoryInterface import \
    BannedTriviaGameControllersRepositoryInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


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
            self.__timber.log('AddBannedTriviaControllerChatCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} tried using this command!')
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('AddBannedTriviaControllerChatCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {ctx.getTwitchChannelName()}, but no arguments were supplied')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to add banned trivia controller as no username argument was given. Example: !addbannedtriviacontroller {administrator}')
            return

        userName = utils.removePreceedingAt(splits[1])
        if not utils.isValidStr(userName):
            self.__timber.log('AddBannedTriviaControllerChatCommand', f'Attempted to handle command for {userName}:{ctx.getAuthorId()} in {user.handle}, but username argument is malformed: \"{userName}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to add banned trivia controller as username argument is malformed. Example: !addbannedtriviacontroller {user.handle}')
            return

        result = await self.__bannedTriviaGameControllersRepository.addBannedController(
            userName = userName
        )

        match result:
            case AddBannedTriviaGameControllerResult.ADDED:
                await self.__twitchUtils.safeSend(
                    messageable = ctx,
                    message = f'ⓘ Added {userName} as a banned trivia game controller',
                    replyMessageId = await ctx.getMessageId()
                )

            case AddBannedTriviaGameControllerResult.ALREADY_EXISTS:
                await self.__twitchUtils.safeSend(
                    messageable = ctx,
                    message = f'ⓘ Tried adding {userName} as a banned trivia game controller, but they already were one',
                    replyMessageId = await ctx.getMessageId()
                )

            case AddBannedTriviaGameControllerResult.ERROR:
                await self.__twitchUtils.safeSend(
                    messageable = ctx,
                    message = f'⚠ An error occurred when trying to add {userName} as a banned trivia game controller!',
                    replyMessageId = await ctx.getMessageId()
                )

            case _:
                await self.__twitchUtils.safeSend(
                    messageable = ctx,
                    message = f'⚠ An unknown error occurred when trying to add {userName} as a banned trivia game controller!',
                    replyMessageId = await ctx.getMessageId()
                )

                self.__timber.log('AddBannedTriviaControllerChatCommand', f'Encountered unknown AddBannedTriviaGameControllerResult value ({result}) when trying to add \"{userName}\" as a banned trivia game controller for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
                raise RuntimeError(f'Encountered unknown AddBannedTriviaGameControllerResult value ({result}) when trying to add \"{userName}\" as a banned trivia game controller for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')

        self.__timber.log('AddBannedTriviaControllerChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
