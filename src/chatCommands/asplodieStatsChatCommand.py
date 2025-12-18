from typing import Final

from .absChatCommand import AbsChatCommand
from ..asplodieStats.asplodieStatsPresenter import AsplodieStatsPresenter
from ..asplodieStats.repository.asplodieStatsRepositoryInterface import AsplodieStatsRepositoryInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class AsplodieStatsChatCommand(AbsChatCommand):

    def __init__(
        self,
        asplodieStatsPresenter: AsplodieStatsPresenter,
        asplodieStatsRepository: AsplodieStatsRepositoryInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
    ):
        if not isinstance(asplodieStatsPresenter, AsplodieStatsPresenter):
            raise TypeError(f'asplodieStatsPresenter argument is malformed: \"{asplodieStatsPresenter}\"')
        elif not isinstance(asplodieStatsRepository, AsplodieStatsRepositoryInterface):
            raise TypeError(f'asplodieStatsRepository argument is malformed: \"{asplodieStatsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__asplodieStatsPresenter: Final[AsplodieStatsPresenter] = asplodieStatsPresenter
        self.__asplodieStatsRepository: Final[AsplodieStatsRepositoryInterface] = asplodieStatsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.areAsplodieStatsEnabled:
            return

        userId = ctx.getAuthorId()
        userName = ctx.getAuthorName()
        splits = utils.getCleanedSplits(ctx.getMessageContent())

        if len(splits) >= 2 and utils.strContainsAlphanumericCharacters(splits[1]):
            userName = utils.removePreceedingAt(splits[1])

        # this means that a user is querying for another user's asplodie stats
        if userName.casefold() != ctx.getAuthorName().casefold():
            userId = await self.__userIdsRepository.fetchUserId(userName = userName)

            if not utils.isValidStr(userId):
                self.__timber.log('AsplodieStatsChatCommand', f'Unable to find user ID for \"{userName}\" in the database')
                self.__twitchChatMessenger.send(
                    text = f'⚠ Unable to find asplodie stats score for \"{userName}\"',
                    twitchChannelId = await ctx.getTwitchChannelId(),
                    replyMessageId = await ctx.getMessageId(),
                )
                return

        asplodieStats = await self.__asplodieStatsRepository.get(
            chatterUserId = userId,
            twitchChannelId = await ctx.getTwitchChannelId(),
        )

        printOut = await self.__asplodieStatsPresenter.printOut(
            asplodieStats = asplodieStats,
            chatterUserName = userName,
        )

        self.__twitchChatMessenger.send(
            text = f'ⓘ Asplodie stats for @{userName} — {printOut}',
            twitchChannelId = await ctx.getTwitchChannelId(),
            replyMessageId = await ctx.getMessageId(),
        )

        self.__timber.log('AsplodieStatsChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
