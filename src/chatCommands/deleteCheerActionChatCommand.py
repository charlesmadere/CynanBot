from .absChatCommand import AbsChatCommand
from ..cheerActions.cheerActionIdGeneratorInterface import \
    CheerActionIdGeneratorInterface
from ..cheerActions.cheerActionsRepositoryInterface import \
    CheerActionsRepositoryInterface
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class DeleteCheerActionChatCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        cheerActionIdGenerator: CheerActionIdGeneratorInterface,
        cheerActionsRepository: CheerActionsRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise ValueError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(cheerActionIdGenerator, CheerActionIdGeneratorInterface):
            raise ValueError(f'cheerActionIdGenerator argument is malformed: \"{cheerActionIdGenerator}\"')
        elif not isinstance(cheerActionsRepository, CheerActionsRepositoryInterface):
            raise ValueError(f'cheerActionsRepository argument is malformed: \"{cheerActionsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__cheerActionIdGenerator: CheerActionIdGeneratorInterface = cheerActionIdGenerator
        self.__cheerActionsRepository: CheerActionsRepositoryInterface = cheerActionsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        userId = await self.__userIdsRepository.requireUserId(user.getHandle())
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if userId != ctx.getAuthorId() and administrator != ctx.getAuthorId():
            self.__timber.log('DeleteCheerActionCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return
        elif not user.areCheerActionsEnabled():
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2 or not utils.strContainsAlphanumericCharacters(splits[1]):
            self.__timber.log('DeleteCheerActionCommand', f'Incorrect arguments given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
            actionId = await self.__cheerActionIdGenerator.generateActionId()
            await self.__twitchUtils.safeSend(ctx, f'⚠ Action ID is necessary for the !deletecheeraction command. Example: !deletecheeraction {actionId}')
            return

        actionId = splits[1]

        action = await self.__cheerActionsRepository.deleteAction(
            actionId = splits[1],
            userId = userId
        )

        if action is None:
            self.__timber.log('DeleteCheerActionCommand', f'Cheer action ID {actionId} was attempted to be deleted by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but no corresponding cheer action was found')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Could not find any corresponding cheer action with ID \"{actionId}\"')
            return

        await self.__twitchUtils.safeSend(ctx, f'ⓘ Deleted cheer action — {action}')
        self.__timber.log('DeleteCheerActionCommand', f'Handled !deletecheeraction command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
