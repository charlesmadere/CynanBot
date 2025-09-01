import traceback
from typing import Final

from .absChatCommand import AbsChatCommand
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..trivia.banned.addBannedTriviaGameControllerResult import \
    AddBannedTriviaGameControllerResult
from ..trivia.banned.bannedTriviaGameControllersRepositoryInterface import \
    BannedTriviaGameControllersRepositoryInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ..twitch.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..users.exceptions import NoSuchUserException
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class AddBannedTriviaControllerChatCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        bannedTriviaGameControllersRepository: BannedTriviaGameControllersRepositoryInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(bannedTriviaGameControllersRepository, BannedTriviaGameControllersRepositoryInterface):
            raise TypeError(f'bannedTriviaGameControllersRepository argument is malformed: \"{timber}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__bannedTriviaGameControllersRepository: Final[BannedTriviaGameControllersRepositoryInterface] = bannedTriviaGameControllersRepository
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()

        if ctx.getAuthorId() != await self.__administratorProvider.getAdministratorUserId():
            self.__timber.log('AddBannedTriviaControllerChatCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} tried using this command!')
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('AddBannedTriviaControllerChatCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {ctx.getTwitchChannelName()}, but no arguments were supplied')

            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to add banned trivia controller as no username argument was given. Example: !addbannedtriviacontroller {twitchHandle}',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
            return

        userName: str | None = utils.removePreceedingAt(splits[1])
        if not utils.isValidStr(userName):
            self.__timber.log('AddBannedTriviaControllerChatCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}, but the username argument is malformed ({userName=})')

            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to add banned trivia controller as username argument is malformed. Example: !addbannedtriviacontroller {twitchHandle}',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
            return

        twitchAccessToken = await self.__twitchTokensRepository.getAccessTokenById(
            twitchChannelId = await ctx.getTwitchChannelId(),
        )

        try:
            userId = await self.__userIdsRepository.requireUserId(
                userName = userName,
                twitchAccessToken = twitchAccessToken,
            )
        except NoSuchUserException as e:
            self.__timber.log('AddBannedTriviaControllerChatCommand', f'Failed to fetch user ID for the given username argument by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} ({userName=})', e, traceback.format_exc())

            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to add banned trivia controller as no user ID could be found for the given username',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
            return

        result = await self.__bannedTriviaGameControllersRepository.addBannedController(userId)

        match result:
            case AddBannedTriviaGameControllerResult.ADDED:
                self.__twitchChatMessenger.send(
                    text = f'ⓘ Added @{userName} as a banned trivia game controller',
                    twitchChannelId = await ctx.getTwitchChannelId(),
                    replyMessageId = await ctx.getMessageId(),
                )

            case AddBannedTriviaGameControllerResult.ALREADY_EXISTS:
                self.__twitchChatMessenger.send(
                    text = f'⚠ Tried adding @{userName} as a banned trivia game controller, but they already were one',
                    twitchChannelId = await ctx.getTwitchChannelId(),
                    replyMessageId = await ctx.getMessageId(),
                )

            case AddBannedTriviaGameControllerResult.ERROR:
                self.__twitchChatMessenger.send(
                    text = f'⚠ An error occurred when trying to add @{userName} as a banned trivia game controller!',
                    twitchChannelId = await ctx.getTwitchChannelId(),
                    replyMessageId = await ctx.getMessageId(),
                )

            case _:
                self.__twitchChatMessenger.send(
                    text = f'⚠ An unknown error occurred when trying to add @{userName} as a banned trivia game controller!',
                    twitchChannelId = await ctx.getTwitchChannelId(),
                    replyMessageId = await ctx.getMessageId(),
                )

                self.__timber.log('AddBannedTriviaControllerChatCommand', f'Encountered unknown AddBannedTriviaGameControllerResult value ({result}) when trying to add \"{userName}\" as a banned trivia game controller for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
                raise ValueError(f'Encountered unknown AddBannedTriviaGameControllerResult value ({result}) when trying to add \"{userName}\" as a banned trivia game controller for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')

        self.__timber.log('AddBannedTriviaControllerChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
