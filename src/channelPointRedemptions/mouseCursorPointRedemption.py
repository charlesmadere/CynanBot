from typing import Final

from .absChannelPointRedemption import AbsChannelPointRedemption
from ..mouseCursor.mouseCursorHelperInterface import MouseCursorHelperInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.localModels.twitchChannelPointsRedemption import TwitchChannelPointsRedemption


class MouseCursorPointRedemption(AbsChannelPointRedemption):

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

    async def handlePointRedemption(
        self,
        channelPointsRedemption: TwitchChannelPointsRedemption,
    ) -> bool:
        twitchUser = channelPointsRedemption.twitchUser
        if not twitchUser.isMouseCursorEnabled:
            return False

        result = await self.__mouseCursorHelper.applyMouseCursor(
            twitchChannel = channelPointsRedemption.twitchChannel,
            twitchChannelId = channelPointsRedemption.twitchChannelId,
        )

        self.__timber.log('MouseCursorPointRedemption', f'Redeemed ({channelPointsRedemption=}) ({result=})')
        return True
