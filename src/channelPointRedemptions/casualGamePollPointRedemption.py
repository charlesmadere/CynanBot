from datetime import timedelta
from typing import Final

from .absChannelPointRedemption import AbsChannelPointRedemption
from ..misc import utils as utils
from ..misc.timedDict import TimedDict
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchChannel import TwitchChannel
from ..twitch.configuration.twitchChannelPointsMessage import TwitchChannelPointsMessage


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
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage,
    ) -> bool:
        twitchUser = twitchChannelPointsMessage.twitchUser
        if not twitchUser.isCasualGamePollEnabled:
            return False

        casualGamePollUrl = twitchUser.casualGamePollUrl
        if not utils.isValidUrl(casualGamePollUrl):
            return False

        twitchChannelId = await twitchChannel.getTwitchChannelId()
        if not self.__lastMessageTimes.isReadyAndUpdate(twitchChannelId):
            return False

        self.__twitchChatMessenger.send(
            text = f'ⓘ Here\'s the current list of casual games: {casualGamePollUrl}',
            twitchChannelId = twitchChannelPointsMessage.twitchChannelId,
        )

        self.__timber.log('CasualGamePollPointRedemption', f'Redeemed casual game poll for {twitchChannelPointsMessage.userName}:{twitchChannelPointsMessage.userId} in {twitchUser.handle}')
        return True
