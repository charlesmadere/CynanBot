from typing import Final

from .absChannelPointsRedemption2 import AbsChannelPointRedemption2
from .pointsRedemptionResult import PointsRedemptionResult
from ..misc import utils as utils
from ..mouseCursor.mouseCursorHelperInterface import MouseCursorHelperInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.localModels.twitchChannelPointsRedemption import TwitchChannelPointsRedemption
from ..users.userInterface import UserInterface


class MouseCursorPointRedemption(AbsChannelPointRedemption2):

    def __init__(
        self,
        mouseCursorHelper: MouseCursorHelperInterface,
        timber: TimberInterface,
    ):
        if not isinstance(mouseCursorHelper, MouseCursorHelperInterface):
            raise TypeError(f'mouseCursorHelper argument is malformed: \"{mouseCursorHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__mouseCursorHelper: Final[MouseCursorHelperInterface] = mouseCursorHelper
        self.__timber: Final[TimberInterface] = timber

    async def handlePointsRedemption(
        self,
        channelPointsRedemption: TwitchChannelPointsRedemption,
    ) -> PointsRedemptionResult:
        twitchUser = channelPointsRedemption.twitchUser
        if not twitchUser.isMouseCursorEnabled:
            return PointsRedemptionResult.IGNORED

        result = await self.__mouseCursorHelper.applyMouseCursor(
            twitchChannel = channelPointsRedemption.twitchChannel,
            twitchChannelId = channelPointsRedemption.twitchChannelId,
        )

        self.__timber.log(self.pointsRedemptionName, f'Redeemed ({result=}) ({channelPointsRedemption=})')
        return PointsRedemptionResult.CONSUMED

    @property
    def pointsRedemptionName(self) -> str:
        return 'MouseCursorPointRedemption'

    def relevantRewardIds(
        self,
        twitchUser: UserInterface,
    ) -> frozenset[str]:
        rewardId = twitchUser.mouseCursorRewardId

        if utils.isValidStr(rewardId):
            return frozenset({ rewardId })
        else:
            return frozenset()
