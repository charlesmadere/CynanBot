import traceback
from typing import Final

from .absChannelPointsRedemption import AbsChannelPointRedemption
from .pointsRedemptionResult import PointsRedemptionResult
from ..cuteness.exceptions import CutenessFeatureIsDisabledException
from ..cuteness.helpers.cutenessHelperInterface import CutenessHelperInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChannelPointsRedemption import TwitchChannelPointsRedemption
from ..users.userInterface import UserInterface


class CutenessPointRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        cutenessHelper: CutenessHelperInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(cutenessHelper, CutenessHelperInterface):
            raise TypeError(f'cutenessHelper argument is malformed: \"{cutenessHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__cutenessHelper: Final[CutenessHelperInterface] = cutenessHelper
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

    async def handlePointsRedemption(
        self,
        pointsRedemption: TwitchChannelPointsRedemption,
    ) -> PointsRedemptionResult:
        twitchUser = pointsRedemption.twitchUser
        if not twitchUser.isCutenessEnabled:
            return PointsRedemptionResult.IGNORED

        cutenessBoosterPacks = twitchUser.cutenessBoosterPacks
        if cutenessBoosterPacks is None or len(cutenessBoosterPacks) == 0:
            return PointsRedemptionResult.IGNORED

        cutenessBoosterPack = cutenessBoosterPacks.get(pointsRedemption.rewardId, None)
        if cutenessBoosterPack is None:
            return PointsRedemptionResult.IGNORED

        try:
            result = await self.__cutenessHelper.fetchCutenessIncrementedBy(
                incrementAmount = cutenessBoosterPack.amount,
                chatterUserId = pointsRedemption.redemptionUserId,
                twitchChannelId = pointsRedemption.twitchChannelId,
            )
        except CutenessFeatureIsDisabledException as e:
            self.__timber.log(self.pointsRedemptionName, f'Failed to increase cuteness as the feature is disabled ({cutenessBoosterPack=}) ({pointsRedemption=})', e, traceback.format_exc())
            return PointsRedemptionResult.IGNORED

        self.__timber.log(self.pointsRedemptionName, f'Redeemed ({result=}) ({cutenessBoosterPack=}) ({pointsRedemption=})')
        return PointsRedemptionResult.CONSUMED

    @property
    def pointsRedemptionName(self) -> str:
        return 'CutenessPointRedemption'

    def relevantRewardIds(
        self,
        twitchUser: UserInterface,
    ) -> frozenset[str]:
        boosterPacks = twitchUser.cutenessBoosterPacks
        rewardIds: set[str] = set()

        if boosterPacks is not None and len(boosterPacks.keys()) >= 1:
            rewardIds.update(boosterPacks.keys())

        return frozenset(rewardIds)
