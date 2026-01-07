from typing import Final

from .absChatCommand import AbsChatCommand
from ..beanStats.beanStatsPresenterInterface import BeanStatsPresenterInterface
from ..beanStats.beanStatsRepositoryInterface import BeanStatsRepositoryInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class BeanStatsChatCommand(AbsChatCommand):

    def __init__(
        self,
        beanStatsPresenter: BeanStatsPresenterInterface,
        beanStatsRepository: BeanStatsRepositoryInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
    ):
        if not isinstance(beanStatsPresenter, BeanStatsPresenterInterface):
            raise TypeError(f'beanStatsPresenter argument is malformed: \"{beanStatsPresenter}\"')
        elif not isinstance(beanStatsRepository, BeanStatsRepositoryInterface):
            raise TypeError(f'beanStatsRepository argument is malformed: \"{beanStatsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__beanStatsPresenter: Final[BeanStatsPresenterInterface] = beanStatsPresenter
        self.__beanStatsRepository: Final[BeanStatsRepositoryInterface] = beanStatsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

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
                self.__twitchChatMessenger.send(
                    text = f'⚠ Unable to find bean stats score for \"{userName}\"',
                    twitchChannelId = await ctx.getTwitchChannelId(),
                    replyMessageId = await ctx.getMessageId(),
                )
                return

        beanStats = await self.__beanStatsRepository.getStats(
            chatterUserId = userId,
            chatterUserName = userName,
            twitchChannel = user.handle,
            twitchChannelId = await ctx.getTwitchChannelId(),
        )

        if beanStats is None:
            self.__twitchChatMessenger.send(
                text = f'ⓘ @{userName} has no bean stats',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
        else:
            printOut = await self.__beanStatsPresenter.toString(beanStats)

            self.__twitchChatMessenger.send(
                text = printOut,
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )

        self.__timber.log('BeanStatsChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
