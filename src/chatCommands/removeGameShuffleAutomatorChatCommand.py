from .absChatCommand import AbsChatCommand
from ..crowdControl.automator.crowdControlAutomatorInterface import CrowdControlAutomatorInterface
from ..crowdControl.automator.crowdControlAutomatorRemovalResult import CrowdControlAutomatorRemovalResult
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class RemoveGameShuffleAutomatorChatCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        crowdControlAutomator: CrowdControlAutomatorInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        if not isinstance(crowdControlAutomator, CrowdControlAutomatorInterface):
            raise TypeError(f'crowdControlAutomator argument is malformed: \"{crowdControlAutomator}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__crowdControlAutomator: CrowdControlAutomatorInterface = crowdControlAutomator
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        userId = await ctx.getTwitchChannelId()
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if userId != ctx.getAuthorId() and administrator != ctx.getAuthorId():
            self.__timber.log('RemoveGameShuffleAutomatorChatCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} tried using this command!')
            return
        elif not user.isCrowdControlEnabled:
            return

        result = await self.__crowdControlAutomator.removeGameShuffleAutomator(
            twitchChannelId = await ctx.getTwitchChannelId()
        )

        match result:
            case CrowdControlAutomatorRemovalResult.DID_NOT_EXIST:
                await self.__twitchUtils.safeSend(
                    messageable = ctx,
                    message = f'ⓘ Attempted to remove the game shuffle automator, but one did not already exist',
                    replyMessageId = await ctx.getMessageId()
                )

            case CrowdControlAutomatorRemovalResult.OK:
                await self.__twitchUtils.safeSend(
                    messageable = ctx,
                    message = f'ⓘ Removed game shuffle automator',
                    replyMessageId = await ctx.getMessageId()
                )

            case _:
                raise RuntimeError(f'Uknown CrowdControlAutomatorRemovalResult: \"{result}\"')

        self.__timber.log('RemoveGameShuffleAutomatorChatCommand', f'Handled !removegameshuffleautomator command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
