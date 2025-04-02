from .absChatCommand import AbsChatCommand
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..trivia.banned.bannedTriviaGameControllersRepositoryInterface import BannedTriviaGameControllersRepositoryInterface
from ..trivia.banned.removeBannedTriviaGameControllerResult import RemoveBannedTriviaGameControllerResult
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class RemoveBannedTriviaControllerChatCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        bannedTriviaGameControllersRepository: BannedTriviaGameControllersRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProviderInterface argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(bannedTriviaGameControllersRepository, BannedTriviaGameControllersRepositoryInterface):
            raise TypeError(f'bannedTriviaGameControllersRepository argument is malformed: \"{bannedTriviaGameControllersRepository}\"')
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
            self.__timber.log('RemoveBannedTriviaControllerChatCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} tried using this command!')
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('RemoveBannedTriviaControllerChatCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}, but no arguments were supplied')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to remove banned trivia controller as no username argument was given. Example: !removebannedtriviacontroller {user.handle}')
            return

        userName: str | None = utils.removePreceedingAt(splits[1])
        if not utils.isValidStr(userName):
            self.__timber.log('RemoveBannedTriviaControllerChatCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}, but username argument is malformed: \"{userName}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to remove banned trivia controller as username argument is malformed. Example: !removebannedtriviacontroller {user.handle}')
            return

        result = await self.__bannedTriviaGameControllersRepository.removeBannedController(
            userName = userName
        )

        match result:
            case RemoveBannedTriviaGameControllerResult.ERROR:
                await self.__twitchUtils.safeSend(
                    messageable = ctx,
                    message = f'⚠ An error occurred when trying to remove @{userName} as a banned trivia game controller!',
                    replyMessageId = await ctx.getMessageId()
                )

            case RemoveBannedTriviaGameControllerResult.NOT_BANNED:
                await self.__twitchUtils.safeSend(
                    messageable = ctx,
                    message = f'⚠ @{userName} is not a banned trivia controller',
                    replyMessageId = await ctx.getMessageId()
                )

            case RemoveBannedTriviaGameControllerResult.REMOVED:
                await self.__twitchUtils.safeSend(
                    messageable = ctx,
                    message = f'ⓘ Removed @{userName} as a banned trivia game controller',
                    replyMessageId = await ctx.getMessageId()
                )

            case _:
                await self.__twitchUtils.safeSend(
                    messageable = ctx,
                    message = f'⚠ An unknown error occurred when trying to remove @{userName} as a banned trivia game controller!',
                    replyMessageId = await ctx.getMessageId()
                )

                self.__timber.log('RemoveBannedTriviaControllerChatCommand', f'Encountered unknown RemoveBannedTriviaGameControllerResult value ({result}) when trying to remove \"{userName}\" as a banned trivia game controller for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
                raise ValueError(f'Encountered unknown RemoveBannedTriviaGameControllerResult value ({result}) when trying to remove \"{userName}\" as a banned trivia game controller for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')

        self.__timber.log('RemoveBannedTriviaControllerChatCommand', f'Handled command with {result} result for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
