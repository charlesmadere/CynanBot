from datetime import timedelta
from typing import Final

from .absChatCommand import AbsChatCommand
from ..misc import utils as utils
from ..misc.timedDict import TimedDict
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class BlueSkyChatCommand(AbsChatCommand):

    def __init__(
        self,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        usersRepository: UsersRepositoryInterface,
        cooldown: timedelta = timedelta(minutes = 1),
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise TypeError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository
        self.__lastMessageTimes: Final[TimedDict] = TimedDict(cooldown)

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        blueSkyUrl = user.blueSkyUrl

        if not utils.isValidUrl(blueSkyUrl):
            return
        elif not ctx.isAuthorMod and not ctx.isAuthorVip and not self.__lastMessageTimes.isReadyAndUpdate(user.handle):
            return

        self.__twitchChatMessenger.send(
            text = f'ⓘ BlueSky: {blueSkyUrl}',
            twitchChannelId = await ctx.getTwitchChannelId(),
            replyMessageId = await ctx.getMessageId(),
        )

        self.__timber.log('BlueSkyChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
