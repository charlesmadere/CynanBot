from datetime import timedelta
from typing import Final

from .absChannelPointsRedemption import AbsChannelPointRedemption
from .pointsRedemptionResult import PointsRedemptionResult
from ..misc import utils as utils
from ..misc.timedDict import TimedDict
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChannelPointsRedemption import TwitchChannelPointsRedemption
from ..users.userInterface import UserInterface


class CasualGamePollPointRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        cooldown: timedelta = timedelta(minutes = 1, seconds = 30),
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

    async def handlePointsRedemption(
        self,
        pointsRedemption: TwitchChannelPointsRedemption,
    ) -> PointsRedemptionResult:
        twitchUser = pointsRedemption.twitchUser
        if not twitchUser.isCasualGamePollEnabled:
            return PointsRedemptionResult.IGNORED

        casualGamePollUrl = twitchUser.casualGamePollUrl
        if not utils.isValidUrl(casualGamePollUrl):
            return PointsRedemptionResult.IGNORED

        if not self.__lastMessageTimes.isReadyAndUpdate(pointsRedemption.twitchChannelId):
            return PointsRedemptionResult.IGNORED

        self.__twitchChatMessenger.send(
            text = f'ⓘ Here\'s the current list of casual games: {casualGamePollUrl}',
            twitchChannelId = pointsRedemption.twitchChannelId,
        )

        self.__timber.log(self.pointsRedemptionName, f'Redeemed ({pointsRedemption=})')
        return PointsRedemptionResult.CONSUMED

    @property
    def pointsRedemptionName(self) -> str:
        return 'CasualGamePollPointRedemption'

    def relevantRewardIds(
        self,
        twitchUser: UserInterface,
    ) -> frozenset[str]:
        rewardId = twitchUser.casualGamePollRewardId

        if utils.isValidStr(rewardId):
            return frozenset({ rewardId })
        else:
            return frozenset()
