from datetime import timedelta

from .absChatCommand import AbsChatCommand
from ..misc import utils as utils
from ..misc.timedDict import TimedDict
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class BlueSkyChatCommand(AbsChatCommand):

    def __init__(
        self,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        cooldown: timedelta = timedelta(minutes = 1)
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise TypeError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        blueSkyUrl = user.blueSkyUrl

        if not utils.isValidUrl(blueSkyUrl):
            return
        elif not ctx.isAuthorMod and not ctx.isAuthorVip and not self.__lastMessageTimes.isReadyAndUpdate(user.handle):
            return

        await self.__twitchUtils.safeSend(
            messageable = ctx,
            message = f'ⓘ BlueSky: {blueSkyUrl}',
            replyMessageId = await ctx.getMessageId()
        )

        self.__timber.log('BlueSkyChatCommand', f'Handled !bluesky command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
