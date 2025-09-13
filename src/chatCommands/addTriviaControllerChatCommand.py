from typing import Final

from .absChatCommand import AbsChatCommand
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..misc.generalSettingsRepository import GeneralSettingsRepository
from ..timber.timberInterface import TimberInterface
from ..trivia.gameController.addTriviaGameControllerResult import AddTriviaGameControllerResult
from ..trivia.gameController.triviaGameControllersRepositoryInterface import TriviaGameControllersRepositoryInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class AddTriviaControllerChatCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        triviaGameControllersRepository: TriviaGameControllersRepositoryInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        usersRepository: UsersRepositoryInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise TypeError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameControllersRepository, TriviaGameControllersRepositoryInterface):
            raise TypeError(f'triviaGameControllersRepository argument is malformed: \"{triviaGameControllersRepository}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__generalSettingsRepository: Final[GeneralSettingsRepository] = generalSettingsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__triviaGameControllersRepository: Final[TriviaGameControllersRepositoryInterface] = triviaGameControllersRepository
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

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
            self.__timber.log('AddTriviaGameControllerChatCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} tried using this command!')
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('AddTriviaGameControllerCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}, but no arguments were supplied')
            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to add trivia controller as no username argument was given. Example: !addtriviacontroller {twitchHandle}',
                twitchChannelId = twitchChannelId,
                replyMessageId = await ctx.getMessageId(),
            )
            return

        userName: str | None = utils.removePreceedingAt(splits[1])
        if not utils.isValidStr(userName):
            self.__timber.log('AddTriviaGameControllerCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}, but username argument is malformed: \"{userName}\"')
            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to add trivia controller as username argument is malformed. Example: !addtriviacontroller {twitchHandle}',
                twitchChannelId = twitchChannelId,
                replyMessageId = await ctx.getMessageId(),
            )
            return

        result = await self.__triviaGameControllersRepository.addController(
            twitchChannel = user.handle,
            twitchChannelId = twitchChannelId,
            userName = userName,
        )

        match result:
            case AddTriviaGameControllerResult.ADDED:
                self.__twitchChatMessenger.send(
                    text = f'ⓘ Added @{userName} as a trivia game controller',
                    twitchChannelId = twitchChannelId,
                    replyMessageId = await ctx.getMessageId(),
                )

            case AddTriviaGameControllerResult.ALREADY_EXISTS:
                self.__twitchChatMessenger.send(
                    text = f'⚠ Tried adding @{userName} as a trivia game controller, but they already were one',
                    twitchChannelId = twitchChannelId,
                    replyMessageId = await ctx.getMessageId(),
                )

            case AddTriviaGameControllerResult.ERROR:
                self.__twitchChatMessenger.send(
                    text = f'⚠ An error occurred when trying to add @{userName} as a trivia game controller!',
                    twitchChannelId = twitchChannelId,
                    replyMessageId = await ctx.getMessageId(),
                )

        self.__timber.log('AddTriviaControllerChatCommand', f'Handled command with {result} result for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
