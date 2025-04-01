import locale
from typing import Final

from .absChatCommand import AbsChatCommand
from ..recentGrenadeAttacks.helper.recentGrenadeAttacksHelperInterface import RecentGrenadeAttacksHelperInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class AvailableGrenadesChatCommand(AbsChatCommand):

    def __init__(
        self,
        recentGrenadeAttacksHelper: RecentGrenadeAttacksHelperInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(recentGrenadeAttacksHelper, RecentGrenadeAttacksHelperInterface):
            raise TypeError(f'recentGrenadeAttacksHelper argument is malformed: \"{recentGrenadeAttacksHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__recentGrenadeAttacksHelper: Final[RecentGrenadeAttacksHelperInterface] = recentGrenadeAttacksHelper
        self.__timber: Final[TimberInterface] = timber
        self.__twitchUtils: Final[TwitchUtilsInterface] = twitchUtils
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        availableGrenades = await self.__recentGrenadeAttacksHelper.fetchAvailableGrenades(
            attackerUserId = ctx.getAuthorId(),
            twitchChannel = user.handle,
            twitchChannelId = await ctx.getTwitchChannelId()
        )

        if availableGrenades is None:
            self.__timber.log('AvailableGrenadesChatCommand', f'This channel has no specified maximum grenades value ({ctx.getAuthorName()}:{ctx.getAuthorId()}) ({availableGrenades=}) ({user=})')
            return

        availableGrenadesString = locale.format_string("%d", availableGrenades, grouping = True)

        grenadesPluralization: str
        if availableGrenades == 1:
            grenadesPluralization = 'grenade'
        else:
            grenadesPluralization = 'grenades'

        await self.__twitchUtils.safeSend(
            messageable = ctx,
            message = f'ⓘ You have {availableGrenadesString} {grenadesPluralization} available',
            replyMessageId = await ctx.getMessageId()
        )

        self.__timber.log('AvailableGrenadesChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
