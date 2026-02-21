from typing import Final

from .absChannelPointRedemption import AbsChannelPointRedemption
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChannelPointsRedemption import TwitchChannelPointsRedemption


class MouseCursorPointRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        visibilityDurationSeconds: int = 16,
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not utils.isValidInt(visibilityDurationSeconds):
            raise TypeError(f'visibilityDurationSeconds argument is malformed: \"{visibilityDurationSeconds}\"')
        elif visibilityDurationSeconds < 1 or visibilityDurationSeconds > 300:
            raise ValueError(f'visibilityDurationSeconds argument is out of bounds: {visibilityDurationSeconds}')

        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__visibilityDurationSeconds: Final[int] = visibilityDurationSeconds

    async def handlePointRedemption(
        self,
        channelPointsRedemption: TwitchChannelPointsRedemption,
    ) -> bool:
        twitchUser = channelPointsRedemption.twitchUser
        if not twitchUser.isMouseCursorEnabled:
            return False

        self.__timber.log('MouseCursorPointRedemption', f'Redeemed ({channelPointsRedemption=})')
        return True
