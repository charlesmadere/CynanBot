import traceback
from typing import Final

from .absChannelPointsRedemption2 import AbsChannelPointRedemption2
from .pointsRedemptionResult import PointsRedemptionResult
from ..cuteness.cutenessRepositoryInterface import CutenessRepositoryInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChannelPointsRedemption import TwitchChannelPointsRedemption
from ..users.userInterface import UserInterface


class CutenessPointRedemption(AbsChannelPointRedemption2):

    def __init__(
        self,
        cutenessRepository: CutenessRepositoryInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(cutenessRepository, CutenessRepositoryInterface):
            raise TypeError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__cutenessRepository: Final[CutenessRepositoryInterface] = cutenessRepository
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
            await self.__cutenessRepository.fetchCutenessIncrementedBy(
                incrementAmount = cutenessBoosterPack.amount,
                twitchChannel = pointsRedemption.twitchChannel,
                twitchChannelId = pointsRedemption.twitchChannelId,
                userId = pointsRedemption.redemptionUserId,
                userName = pointsRedemption.redemptionUserName,
            )

            self.__timber.log(self.pointsRedemptionName, f'Redeemed ({cutenessBoosterPack=}) ({pointsRedemption=})')
        except Exception as e:
            self.__timber.log(self.pointsRedemptionName, f'Error redeeming ({cutenessBoosterPack=}) ({pointsRedemption=})', e, traceback.format_exc())
            self.__twitchChatMessenger.send(
                text = f'⚠ Error increasing cuteness for @{pointsRedemption.redemptionUserName}',
                twitchChannelId = pointsRedemption.twitchChannelId,
            )

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
