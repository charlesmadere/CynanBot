import traceback
from typing import Final

from .absChannelPointsRedemption2 import AbsChannelPointRedemption2
from .pointsRedemptionResult import PointsRedemptionResult
from ..chatterPreferredName.exceptions import ChatterPreferredNameFeatureIsDisabledException, \
    ChatterPreferredNameIsInvalidException
from ..chatterPreferredName.helpers.chatterPreferredNameHelperInterface import ChatterPreferredNameHelperInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChannelPointsRedemption import TwitchChannelPointsRedemption
from ..users.userInterface import UserInterface


class ChatterPreferredNamePointRedemption(AbsChannelPointRedemption2):

    def __init__(
        self,
        chatterPreferredNameHelper: ChatterPreferredNameHelperInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(chatterPreferredNameHelper, ChatterPreferredNameHelperInterface):
            raise TypeError(f'chatterPreferredNameHelper argument is malformed: \"{chatterPreferredNameHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__chatterPreferredNameHelper: Final[ChatterPreferredNameHelperInterface] = chatterPreferredNameHelper
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

    async def handlePointsRedemption(
        self,
        channelPointsRedemption: TwitchChannelPointsRedemption,
    ) -> PointsRedemptionResult:
        twitchUser = channelPointsRedemption.twitchUser
        if not twitchUser.isChatterPreferredNameEnabled:
            return PointsRedemptionResult.IGNORED

        try:
            preferredNameData = await self.__chatterPreferredNameHelper.set(
                chatterUserId = channelPointsRedemption.redemptionUserId,
                preferredName = channelPointsRedemption.redemptionMessage,
                twitchChannelId = channelPointsRedemption.twitchChannelId,
            )
        except ChatterPreferredNameFeatureIsDisabledException as e:
            self.__timber.log(self.pointsRedemptionName, f'Preferred name feature is disabled ({channelPointsRedemption=})', e, traceback.format_exc())
            return PointsRedemptionResult.IGNORED
        except ChatterPreferredNameIsInvalidException as e:
            self.__timber.log(self.pointsRedemptionName, f'The given preferred name is invalid ({channelPointsRedemption=})', e, traceback.format_exc())
            self.__twitchChatMessenger.send(
                text = f'⚠ @{channelPointsRedemption.redemptionUserName} unable to set your preferred name! Please check your input and try again.',
                twitchChannelId = channelPointsRedemption.twitchChannelId,
            )
            return PointsRedemptionResult.IGNORED

        self.__twitchChatMessenger.send(
            text = f'ⓘ @{channelPointsRedemption.redemptionUserName} here\'s your new preferred name: {preferredNameData.preferredName}',
            twitchChannelId = channelPointsRedemption.twitchChannelId,
        )

        self.__timber.log(self.pointsRedemptionName, f'Redeemed ({channelPointsRedemption=}) ({preferredNameData=})')
        return PointsRedemptionResult.HANDLED

    @property
    def pointsRedemptionName(self) -> str:
        return 'ChatterPreferredNamePointRedemption'

    def relevantRewardIds(
        self,
        twitchUser: UserInterface,
    ) -> frozenset[str]:
        rewardId = twitchUser.chatterPreferredNameRewardId

        if utils.isValidStr(rewardId):
            return frozenset({ rewardId })
        else:
            return frozenset()
