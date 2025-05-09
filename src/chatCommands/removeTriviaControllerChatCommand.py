from .absChatCommand import AbsChatCommand
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..misc.generalSettingsRepository import GeneralSettingsRepository
from ..timber.timberInterface import TimberInterface
from ..trivia.gameController.removeTriviaGameControllerResult import RemoveTriviaGameControllerResult
from ..trivia.gameController.triviaGameControllersRepositoryInterface import TriviaGameControllersRepositoryInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class RemoveTriviaControllerChatCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        triviaGameControllersRepository: TriviaGameControllersRepositoryInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise TypeError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameControllersRepository, TriviaGameControllersRepositoryInterface):
            raise TypeError(f'triviaGameControllersRepository argument is malformed: \"{triviaGameControllersRepository}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__triviaGameControllersRepository: TriviaGameControllersRepositoryInterface = triviaGameControllersRepository
        self.__twitchHandleProvider: TwitchHandleProviderInterface = twitchHandleProvider
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()
        twitchChannelId = await ctx.getTwitchChannelId()
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if not generalSettings.isTriviaGameEnabled() and not generalSettings.isSuperTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled and not user.isSuperTriviaGameEnabled:
            return

        if twitchChannelId != ctx.getAuthorId() and administrator != ctx.getAuthorId():
            self.__timber.log('RemoveTriviaControllerChatCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} tried using this command!')
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('RemoveTriviaControllerChatCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}, but no arguments were supplied')
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'⚠ Unable to remove trivia controller as no username argument was given. Example: !removetriviacontroller {twitchHandle}',
                replyMessageId = await ctx.getMessageId()
            )
            return

        userName: str | None = utils.removePreceedingAt(splits[1])
        if not utils.isValidStr(userName):
            self.__timber.log('RemoveTriviaControllerChatCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}, but username argument is malformed: \"{userName}\"')
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'⚠ Unable to remove trivia controller as username argument is malformed. Example: !removetriviacontroller {twitchHandle}',
                replyMessageId = await ctx.getMessageId()
            )
            return

        result = await self.__triviaGameControllersRepository.removeController(
            twitchChannel = user.handle,
            twitchChannelId = twitchChannelId,
            userName = userName
        )

        match result:
            case RemoveTriviaGameControllerResult.DOES_NOT_EXIST:
                await self.__twitchUtils.safeSend(
                    messageable = ctx,
                    message = f'⚠ @{userName} is not a trivia game controller',
                    replyMessageId = await ctx.getMessageId()
                )

            case RemoveTriviaGameControllerResult.ERROR:
                await self.__twitchUtils.safeSend(
                    messageable = ctx,
                    message = f'⚠ An error occurred when trying to remove @{userName} as a trivia game controller!',
                    replyMessageId = await ctx.getMessageId()
                )

            case RemoveTriviaGameControllerResult.REMOVED:
                await self.__twitchUtils.safeSend(
                    messageable = ctx,
                    message = f'ⓘ Removed @{userName} as a trivia game controller',
                    replyMessageId = await ctx.getMessageId()
                )

            case _:
                await self.__twitchUtils.safeSend(
                    messageable = ctx,
                    message = f'⚠ An unknown error occurred when trying to remove @{userName} as a trivia game controller!',
                    replyMessageId = await ctx.getMessageId()
                )

                self.__timber.log('RemoveTriviaControllerChatCommand', f'Encountered unknown RemoveTriviaGameControllerResult value ({result}) when trying to remove \"{userName}\" as a trivia game controller for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
                raise ValueError(f'Encountered unknown RemoveTriviaGameControllerResult value ({result}) when trying to remove \"{userName}\" as a trivia game controller for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')

        self.__timber.log('RemoveTriviaControllerChatCommand', f'Handled command with {result} result for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
