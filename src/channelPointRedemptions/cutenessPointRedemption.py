import traceback
from typing import Final

from .absChannelPointRedemption2 import AbsChannelPointRedemption2
from ..cuteness.cutenessRepositoryInterface import CutenessRepositoryInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChannelPointsRedemption import TwitchChannelPointsRedemption


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

    async def handlePointRedemption(
        self,
        channelPointsRedemption: TwitchChannelPointsRedemption,
    ) -> bool:
        twitchUser = channelPointsRedemption.twitchUser
        if not twitchUser.isCutenessEnabled:
            return False

        cutenessBoosterPacks = twitchUser.cutenessBoosterPacks
        if cutenessBoosterPacks is None or len(cutenessBoosterPacks) == 0:
            return False

        cutenessBoosterPack = cutenessBoosterPacks.get(channelPointsRedemption.rewardId, None)
        if cutenessBoosterPack is None:
            return False

        incrementAmount = cutenessBoosterPack.amount

        try:
            await self.__cutenessRepository.fetchCutenessIncrementedBy(
                incrementAmount = incrementAmount,
                twitchChannel = channelPointsRedemption.twitchChannel,
                twitchChannelId = channelPointsRedemption.twitchChannelId,
                userId = channelPointsRedemption.redemptionUserId,
                userName = channelPointsRedemption.redemptionUserName,
            )

            self.__timber.log('CutenessRedemption', f'Redeemed ({channelPointsRedemption=}) ({incrementAmount=})')
        except Exception as e:
            self.__timber.log('CutenessRedemption', f'Error redeeming ({channelPointsRedemption=}) ({incrementAmount=})', e, traceback.format_exc())
            self.__twitchChatMessenger.send(
                text = f'⚠ Error increasing cuteness for @{channelPointsRedemption.redemptionUserName}',
                twitchChannelId = channelPointsRedemption.twitchChannelId,
            )

        return True
