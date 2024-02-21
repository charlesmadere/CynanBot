from datetime import timedelta

import CynanBot.misc.utils as utils
from CynanBot.channelPointRedemptions.absChannelPointRedemption import \
    AbsChannelPointRedemption
from CynanBot.misc.timedDict import TimedDict
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.configuration.twitchChannel import TwitchChannel
from CynanBot.twitch.configuration.twitchChannelPointsMessage import \
    TwitchChannelPointsMessage
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface


class CasualGamePollRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        cooldown: timedelta = timedelta(seconds = 30)
    ):
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"

        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage
    ) -> bool:
        twitchUser = twitchChannelPointsMessage.getTwitchUser()
        if not twitchUser.isCasualGamePollEnabled():
            return False

        casualGamePollUrl = twitchUser.getCasualGamePollUrl()
        if not utils.isValidUrl(casualGamePollUrl):
            return False

        twitchChannelId = await twitchChannel.getTwitchChannelId()
        if not self.__lastMessageTimes.isReadyAndUpdate(twitchChannelId):
            return False

        await self.__twitchUtils.safeSend(twitchChannel, casualGamePollUrl)
        self.__timber.log('CasualGamePollRedemption', f'Redeemed casual game poll for {twitchChannelPointsMessage.getUserName()}:{twitchChannelPointsMessage.getUserId()} in {twitchUser.getHandle()}')
        return True
