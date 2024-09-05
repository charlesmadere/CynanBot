from .absChatCommand import AbsChatCommand
from ..beanStats.beanStatsPresenterInterface import BeanStatsPresenterInterface
from ..beanStats.beanStatsRepositoryInterface import BeanStatsRepositoryInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class BeanStatsChatCommand(AbsChatCommand):

    def __init__(
        self,
        beanStatsPresenter: BeanStatsPresenterInterface,
        beanStatsRepository: BeanStatsRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(beanStatsPresenter, BeanStatsPresenterInterface):
            raise TypeError(f'beanStatsPresenter argument is malformed: \"{beanStatsPresenter}\"')
        elif not isinstance(beanStatsRepository, BeanStatsRepositoryInterface):
            raise TypeError(f'beanStatsRepository argument is malformed: \"{beanStatsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__beanStatsPresenter: BeanStatsPresenterInterface = beanStatsPresenter
        self.__beanStatsRepository: BeanStatsRepositoryInterface = beanStatsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.areBeanChancesEnabled:
            return

        beanStats = await self.__beanStatsRepository.getStats(
            chatterUserId = ctx.getAuthorId(),
            chatterUserName = ctx.getAuthorName(),
            twitchChannel = user.getHandle(),
            twitchChannelId = await ctx.getTwitchChannelId()
        )

        if beanStats is None:
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = 'Sorry, you have no bean stats',
                replyMessageId = await ctx.getMessageId()
            )
            return

        printOut = await self.__beanStatsPresenter.toString(beanStats)

        await self.__twitchUtils.safeSend(
            messageable = ctx,
            message = printOut,
            replyMessageId = await ctx.getMessageId()
        )

        self.__timber.log('BeanStatsChatCommand', f'Handled !beanstats for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
