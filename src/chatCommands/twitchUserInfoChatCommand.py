from typing import Final

from .absChatCommand import AbsChatCommand
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.api.models.twitchFetchUserWithLoginRequest import TwitchFetchUserWithLoginRequest
from ..twitch.api.models.twitchUser import TwitchUser
from ..twitch.api.models.twitchUsersResponse import TwitchUsersResponse
from ..twitch.api.twitchApiServiceInterface import TwitchApiServiceInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.handleProvider.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class TwitchUserInfoChatCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        timber: TimberInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__timber: Final[TimberInterface] = timber
        self.__twitchApiService: Final[TwitchApiServiceInterface] = twitchApiService
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if ctx.getAuthorId() != administrator:
            self.__timber.log('TwitchInfoCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} tried using this command!')
            return

        twitchAccessToken = await self.__twitchTokensRepository.getAccessTokenById(
            twitchChannelId = await ctx.getTwitchChannelId(),
        )

        if not utils.isValidStr(twitchAccessToken):
            twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()
            twitchAccessToken = await self.__twitchTokensRepository.getAccessToken(twitchHandle)

            if not utils.isValidStr(twitchAccessToken):
                self.__timber.log('TwitchInfoCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}, but was unable to retrieve a valid Twitch access token')
                self.__twitchChatMessenger.send(
                    text = f'⚠ Unable to retrieve a valid Twitch access token to use with this command!',
                    twitchChannelId = await ctx.getTwitchChannelId(),
                    replyMessageId = await ctx.getMessageId(),
                )
                return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('TwitchInfoCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}, but no arguments were supplied')
            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to retrieve Twitch info as no username argument was given. Example: !twitchinfo {user.handle}',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
            return

        userName: str | None = splits[1]
        if not utils.isValidStr(userName) or not utils.strContainsAlphanumericCharacters(userName):
            self.__timber.log('TwitchInfoCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}, but no arguments were supplied')
            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to retrieve Twitch info as no username argument was given. Example: !twitchinfo {user.handle}',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
            return

        usersResponse: TwitchUsersResponse | None = None
        twitchUser: TwitchUser | None = None
        exception: Exception | None = None

        try:
            usersResponse = await self.__twitchApiService.fetchUser(
                twitchAccessToken = twitchAccessToken,
                fetchUserRequest = TwitchFetchUserWithLoginRequest(
                    userLogin = userName,
                )
            )
        except Exception as e:
            exception = e

        if usersResponse is not None:
            for dataElement in usersResponse.data:
                if dataElement.userLogin.casefold() == userName.casefold():
                    twitchUser = dataElement
                    break

        if twitchUser is None or exception is not None:
            self.__timber.log('TwitchInfoCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}, but the TwitchApiService call failed ({userName=}) ({usersResponse=}) ({twitchUser=}) ({exception=})')
            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to retrieve Twitch info for \"{userName}\" as the Twitch API service call failed',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
            return

        userInfoStr = await self.__toStr(
            twitchUser = twitchUser,
        )

        self.__twitchChatMessenger.send(
            text = f'ⓘ Twitch info for {userName} — {userInfoStr}',
            twitchChannelId = await ctx.getTwitchChannelId(),
            replyMessageId = await ctx.getMessageId(),
        )

        self.__timber.log('TwitchInfoCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')

    async def __toStr(self, twitchUser: TwitchUser) -> str:
        if not isinstance(twitchUser, TwitchUser):
            raise TypeError(f'twitchUser argument is malformed: \"{twitchUser}\"')

        broadcasterType = twitchUser.broadcasterType
        displayName = twitchUser.displayName
        userId = twitchUser.userId
        userType = twitchUser.userType
        return f'broadcasterType:\"{broadcasterType}\", displayName:\"{displayName}\", userId:\"{userId}\", userType:\"{userType}\"'
