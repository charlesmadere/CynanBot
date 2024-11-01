from .absChannelPointRedemption import AbsChannelPointRedemption
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchChannel import TwitchChannel
from ..twitch.configuration.twitchChannelPointsMessage import TwitchChannelPointsMessage
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface


class ShizaPointRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        shizaMessageDelay: int = 5,
        shizaMessage: str | None = 'Shiza'
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not utils.isValidInt(shizaMessageDelay):
            raise TypeError(f'shizaMessageDelay argument is malformed: \"{shizaMessageDelay}\"')
        elif shizaMessageDelay < 0 or shizaMessageDelay >= utils.getIntMaxSafeSize():
            raise ValueError(f'shizaMessageDelay argument is out of bounds: {shizaMessageDelay}')
        elif shizaMessage is not None and not isinstance(shizaMessage, str):
            raise TypeError(f'shizaMessage argument is malformed: \"{shizaMessage}\"')

        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__shizaMessageDelay: int = shizaMessageDelay
        self.__shizaMessage: str | None = shizaMessage

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage
    ) -> bool:
        shizaMessage = self.__shizaMessage
        twitchUser = twitchChannelPointsMessage.twitchUser
        shizaMessageRewardId = twitchUser.shizaMessageRewardId

        if not twitchUser.isShizaMessageEnabled:
            return False
        elif not utils.isValidStr(shizaMessage):
            return False
        elif not utils.isValidStr(shizaMessageRewardId):
            return False
        elif shizaMessageRewardId != twitchChannelPointsMessage.rewardId:
            return False

        await self.__twitchUtils.waitThenSend(
            messageable = twitchChannel,
            delaySeconds = self.__shizaMessageDelay,
            message = shizaMessage
        )

        return True
