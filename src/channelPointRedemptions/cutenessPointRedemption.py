import traceback

from .absChannelPointRedemption import AbsChannelPointRedemption
from ..cuteness.cutenessRepositoryInterface import CutenessRepositoryInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchChannel import TwitchChannel
from ..twitch.configuration.twitchChannelPointsMessage import TwitchChannelPointsMessage
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface


class CutenessPointRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        cutenessRepository: CutenessRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface
    ):
        if not isinstance(cutenessRepository, CutenessRepositoryInterface):
            raise TypeError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__cutenessRepository: CutenessRepositoryInterface = cutenessRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage
    ) -> bool:
        twitchUser = twitchChannelPointsMessage.getTwitchUser()

        if not twitchUser.isCutenessEnabled():
            return False

        cutenessBoosterPacks = twitchUser.cutenessBoosterPacks
        if cutenessBoosterPacks is None or len(cutenessBoosterPacks) == 0:
            return False

        cutenessBoosterPack = cutenessBoosterPacks.get(twitchChannelPointsMessage.getRewardId(), None)
        if cutenessBoosterPack is None:
            return False

        incrementAmount = cutenessBoosterPack.amount

        try:
            await self.__cutenessRepository.fetchCutenessIncrementedBy(
                incrementAmount = incrementAmount,
                twitchChannel = twitchUser.getHandle(),
                twitchChannelId = await twitchChannel.getTwitchChannelId(),
                userId = twitchChannelPointsMessage.getUserId(),
                userName = twitchChannelPointsMessage.getUserName()
            )

            self.__timber.log('CutenessRedemption', f'Redeemed cuteness of {incrementAmount} for {twitchChannelPointsMessage.getUserName()}:{twitchChannelPointsMessage.getUserId()} in {twitchUser.getHandle()}')
        except (OverflowError, ValueError) as e:
            self.__timber.log('CutenessRedemption', f'Error redeeming cuteness of {incrementAmount} for {twitchChannelPointsMessage.getUserName()}:{twitchChannelPointsMessage.getUserId()} in {twitchUser.getHandle()}: {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(twitchChannel, f'⚠ Error increasing cuteness for {twitchChannelPointsMessage.getUserName()}')

        return True
