from typing import Final

from .absChannelPointRedemption import AbsChannelPointRedemption
from ..funtoon.funtoonHelperInterface import FuntoonHelperInterface
from ..funtoon.funtoonPkmnCatchType import FuntoonPkmnCatchType
from ..misc.generalSettingsRepository import GeneralSettingsRepository
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChannelPointsRedemption import TwitchChannelPointsRedemption
from ..users.pkmn.pkmnCatchBoosterPack import PkmnCatchBoosterPack
from ..users.pkmn.pkmnCatchType import PkmnCatchType


class PkmnCatchPointRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        funtoonHelper: FuntoonHelperInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(funtoonHelper, FuntoonHelperInterface):
            raise TypeError(f'funtoonHelper argument is malformed: \"{funtoonHelper}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise TypeError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__funtoonHelper: Final[FuntoonHelperInterface] = funtoonHelper
        self.__generalSettingsRepository: Final[GeneralSettingsRepository] = generalSettingsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

    async def handlePointRedemption(
        self,
        channelPointsRedemption: TwitchChannelPointsRedemption,
    ) -> bool:
        twitchUser = channelPointsRedemption.twitchUser
        if not twitchUser.isPkmnEnabled:
            return False

        pkmnCatchBoosterPacks = twitchUser.pkmnCatchBoosterPacks
        if pkmnCatchBoosterPacks is None or len(pkmnCatchBoosterPacks) == 0:
            return False

        pkmnCatchBoosterPack = pkmnCatchBoosterPacks.get(channelPointsRedemption.rewardId, None)
        if pkmnCatchBoosterPack is None:
            return False

        funtoonPkmnCatchType: FuntoonPkmnCatchType | None = None
        if pkmnCatchBoosterPack.catchType is not None:
            funtoonPkmnCatchType = self.__toFuntoonPkmnCatchType(pkmnCatchBoosterPack)

        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        actionCompleted = False

        if generalSettings.isFuntoonApiEnabled() and await self.__funtoonHelper.pkmnCatch(
            twitchChannel = channelPointsRedemption.twitchChannel,
            twitchChannelId = channelPointsRedemption.twitchChannelId,
            userThatRedeemed = channelPointsRedemption.redemptionUserName,
            funtoonPkmnCatchType = funtoonPkmnCatchType,
        ):
            actionCompleted = True

        if not actionCompleted and generalSettings.isFuntoonTwitchChatFallbackEnabled():
            self.__twitchChatMessenger.send(
                text = f'!catch {channelPointsRedemption.redemptionUserName}',
                twitchChannelId = channelPointsRedemption.twitchChannelId,
            )
            actionCompleted = True

        self.__timber.log('PkmnCatchRedemption', f'Redeemed ({pkmnCatchBoosterPack=}) ({actionCompleted=})')
        return actionCompleted

    def __toFuntoonPkmnCatchType(
        self,
        pkmnCatchBoosterPack: PkmnCatchBoosterPack,
    ) -> FuntoonPkmnCatchType:
        if not isinstance(pkmnCatchBoosterPack, PkmnCatchBoosterPack):
            raise TypeError(f'pkmnCatchBoosterPack argument is malformed: \"{pkmnCatchBoosterPack}\"')

        match pkmnCatchBoosterPack.catchType:
            case PkmnCatchType.GREAT: return FuntoonPkmnCatchType.GREAT
            case PkmnCatchType.NORMAL: return FuntoonPkmnCatchType.NORMAL
            case PkmnCatchType.ULTRA: return FuntoonPkmnCatchType.ULTRA
            case _: raise ValueError(f'unknown PkmnCatchType: \"{pkmnCatchBoosterPack.catchType}\"')
