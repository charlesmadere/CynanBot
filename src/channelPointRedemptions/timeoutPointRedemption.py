from .absChannelPointRedemption import AbsChannelPointRedemption
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..timeout.timeoutActionHelperInterface import TimeoutActionHelperInterface
from ..twitch.configuration.twitchChannel import TwitchChannel
from ..twitch.configuration.twitchChannelPointsMessage import TwitchChannelPointsMessage
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface


class TimeoutPointRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        timber: TimberInterface,
        timeoutActionHelper: TimeoutActionHelperInterface,
        twitchUtils: TwitchUtilsInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutActionHelper, TimeoutActionHelperInterface):
            raise TypeError(f'timeoutActionHelper argument is malformed: \"{timeoutActionHelper}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__timber: TimberInterface = timber
        self.__timeoutActionHelper: TimeoutActionHelperInterface = timeoutActionHelper
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage
    ) -> bool:
        twitchUser = twitchChannelPointsMessage.twitchUser
        if not twitchUser.areTimeoutActionsEnabled:
            return False

        # TODO
        return False
