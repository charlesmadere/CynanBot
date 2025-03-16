from .absChatCommand import AbsChatCommand
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.addOrRemoveUserActionType import AddOrRemoveUserActionType
from ..users.addOrRemoveUserDataHelperInterface import AddOrRemoveUserDataHelperInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class AddUserChatCommand(AbsChatCommand):

    def __init__(
        self,
        addOrRemoveDataHelper: AddOrRemoveUserDataHelperInterface,
        administratorProvider: AdministratorProviderInterface,
        timber: TimberInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(addOrRemoveDataHelper, AddOrRemoveUserDataHelperInterface):
            raise TypeError(f'addOrRemoveDataHelper argument is malformed: \"{addOrRemoveDataHelper}\"')
        elif not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__addOrRemoveUserDataHelper: AddOrRemoveUserDataHelperInterface = addOrRemoveDataHelper
        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__timber: TimberInterface = timber
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if ctx.getAuthorId() != administrator:
            self.__timber.log('AddUserCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} tried using this command!')
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('AddUserCommand', f'Not enough arguments given by {ctx.getAuthorName()}:{ctx.getAuthorId()} for the !adduser command: \"{splits}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Username argument is necessary for the !adduser command. Example: !adduser {user.handle}')
            return

        userName: str | None = utils.removePreceedingAt(splits[1])
        if not utils.isValidStr(userName):
            self.__timber.log('AddUserCommand', f'Invalid username argument given by {ctx.getAuthorName()}:{ctx.getAuthorId()} for the !adduser command: \"{splits}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Username argument is necessary for the !adduser command. Example: !adduser {user.handle}')
            return

        if await self.__usersRepository.containsUserAsync(userName):
            self.__timber.log('AddUserCommand', f'Username argument (\"{userName}\") given by {ctx.getAuthorName()}:{ctx.getAuthorId()} already exists as a user')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to add \"{userName}\" as this user already exists!')
            return

        userId = await self.__userIdsRepository.fetchUserId(
            userName = userName,
            twitchAccessToken = await self.__twitchTokensRepository.getAccessTokenById(
                twitchChannelId = await ctx.getTwitchChannelId()
            )
        )

        if not utils.isValidStr(userId):
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to fetch user ID for \"{userName}\"!')
            return

        await self.__addOrRemoveUserDataHelper.setUserData(
            actionType = AddOrRemoveUserActionType.ADD,
            userId = userId,
            userName = userName
        )

        await self.__twitchUtils.safeSend(ctx, f'ⓘ To add user \"{userName}\" ({userId}), please respond with `!confirm`')
        self.__timber.log('AddUserCommand', f'Handled !adduser command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
