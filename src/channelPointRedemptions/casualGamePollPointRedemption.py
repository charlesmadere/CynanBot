from datetime import timedelta
from typing import Final

from .absChannelPointRedemption import AbsChannelPointRedemption
from ..misc import utils as utils
from ..misc.timedDict import TimedDict
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChannelPointsRedemption import TwitchChannelPointsRedemption


class CasualGamePollPointRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        cooldown: timedelta = timedelta(seconds = 45),
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(cooldown, timedelta):
            raise TypeError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__lastMessageTimes: Final[TimedDict] = TimedDict(cooldown)

    async def handlePointRedemption(
        self,
        channelPointsRedemption: TwitchChannelPointsRedemption,
    ) -> bool:
        twitchUser = channelPointsRedemption.twitchUser
        if not twitchUser.isCasualGamePollEnabled:
            return False

        casualGamePollUrl = twitchUser.casualGamePollUrl
        if not utils.isValidUrl(casualGamePollUrl):
            return False

        if not self.__lastMessageTimes.isReadyAndUpdate(channelPointsRedemption.twitchChannelId):
            return False

        self.__twitchChatMessenger.send(
            text = f'ⓘ Here\'s the current list of casual games: {casualGamePollUrl}',
            twitchChannelId = channelPointsRedemption.twitchChannelId,
        )

        self.__timber.log('CasualGamePollPointRedemption', f'Redeemed ({channelPointsRedemption=})')
        return True
