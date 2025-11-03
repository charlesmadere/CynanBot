import traceback
from typing import Final

from .absChannelPointRedemption import AbsChannelPointRedemption
from ..cuteness.cutenessRepositoryInterface import CutenessRepositoryInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchChannel import TwitchChannel
from ..twitch.configuration.twitchChannelPointsMessage import TwitchChannelPointsMessage


class CutenessPointRedemption(AbsChannelPointRedemption):

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
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage,
    ) -> bool:
        twitchUser = twitchChannelPointsMessage.twitchUser
        if not twitchUser.isCutenessEnabled:
            return False

        cutenessBoosterPacks = twitchUser.cutenessBoosterPacks
        if cutenessBoosterPacks is None or len(cutenessBoosterPacks) == 0:
            return False

        cutenessBoosterPack = cutenessBoosterPacks.get(twitchChannelPointsMessage.rewardId, None)
        if cutenessBoosterPack is None:
            return False

        incrementAmount = cutenessBoosterPack.amount

        try:
            await self.__cutenessRepository.fetchCutenessIncrementedBy(
                incrementAmount = incrementAmount,
                twitchChannel = twitchUser.handle,
                twitchChannelId = await twitchChannel.getTwitchChannelId(),
                userId = twitchChannelPointsMessage.userId,
                userName = twitchChannelPointsMessage.userName
            )

            self.__timber.log('CutenessRedemption', f'Redeemed cuteness of {incrementAmount} for {twitchChannelPointsMessage.userName}:{twitchChannelPointsMessage.userId} in {twitchUser.handle}')
        except Exception as e:
            self.__timber.log('CutenessRedemption', f'Error redeeming cuteness of {incrementAmount} for {twitchChannelPointsMessage.userName}:{twitchChannelPointsMessage.userId} in {twitchUser.handle}: {e}', e, traceback.format_exc())
            self.__twitchChatMessenger.send(
                text = f'⚠ Error increasing cuteness for {twitchChannelPointsMessage.userName}',
                twitchChannelId = twitchChannelPointsMessage.twitchChannelId,
            )

        return True
