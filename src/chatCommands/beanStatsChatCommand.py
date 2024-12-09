from .absChatCommand import AbsChatCommand
from ..beanStats.beanStatsPresenterInterface import BeanStatsPresenterInterface
from ..beanStats.beanStatsRepositoryInterface import BeanStatsRepositoryInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class BeanStatsChatCommand(AbsChatCommand):

    def __init__(
        self,
        beanStatsPresenter: BeanStatsPresenterInterface,
        beanStatsRepository: BeanStatsRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
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
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__beanStatsPresenter: BeanStatsPresenterInterface = beanStatsPresenter
        self.__beanStatsRepository: BeanStatsRepositoryInterface = beanStatsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.areBeanStatsEnabled:
            return

        userId = ctx.getAuthorId()
        userName = ctx.getAuthorName()
        splits = utils.getCleanedSplits(ctx.getMessageContent())

        if len(splits) >= 2 and utils.strContainsAlphanumericCharacters(splits[1]):
            userName = utils.removePreceedingAt(splits[1])

        # this means that a user is querying for another user's bean stats
        if userName.casefold() != ctx.getAuthorName().casefold():
            userId = await self.__userIdsRepository.fetchUserId(userName = userName)

            if not utils.isValidStr(userId):
                await self.__twitchUtils.safeSend(
                    messageable = ctx,
                    message = f'⚠ Unable to find bean stats score for \"{userName}\"',
                    replyMessageId = await ctx.getMessageId()
                )
                return

        beanStats = await self.__beanStatsRepository.getStats(
            chatterUserId = userId,
            chatterUserName = userName,
            twitchChannel = user.handle,
            twitchChannelId = await ctx.getTwitchChannelId()
        )

        if beanStats is None:
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'ⓘ @{userName} has no bean stats',
                replyMessageId = await ctx.getMessageId()
            )
        else:
            printOut = await self.__beanStatsPresenter.toString(beanStats)

            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = printOut,
                replyMessageId = await ctx.getMessageId()
            )

        self.__timber.log('BeanStatsChatCommand', f'Handled !beanstats for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
