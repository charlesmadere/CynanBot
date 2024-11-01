from .absChannelPointRedemption import AbsChannelPointRedemption
from ..funtoon.funtoonPkmnCatchType import FuntoonPkmnCatchType
from ..funtoon.funtoonRepositoryInterface import FuntoonRepositoryInterface
from ..misc.generalSettingsRepository import GeneralSettingsRepository
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchChannel import TwitchChannel
from ..twitch.configuration.twitchChannelPointsMessage import TwitchChannelPointsMessage
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.pkmn.pkmnCatchBoosterPack import PkmnCatchBoosterPack
from ..users.pkmn.pkmnCatchType import PkmnCatchType


class PkmnCatchPointRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        funtoonRepository: FuntoonRepositoryInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface
    ):
        if not isinstance(funtoonRepository, FuntoonRepositoryInterface):
            raise TypeError(f'funtoonRepository argument is malformed: \"{funtoonRepository}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise TypeError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__funtoonRepository: FuntoonRepositoryInterface = funtoonRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage
    ) -> bool:
        twitchUser = twitchChannelPointsMessage.twitchUser
        if not twitchUser.isPkmnEnabled():
            return False

        pkmnCatchBoosterPacks = twitchUser.pkmnCatchBoosterPacks
        if pkmnCatchBoosterPacks is None or len(pkmnCatchBoosterPacks) == 0:
            return False

        pkmnCatchBoosterPack = pkmnCatchBoosterPacks.get(twitchChannelPointsMessage.rewardId, None)
        if pkmnCatchBoosterPack is None:
            return False

        funtoonPkmnCatchType: FuntoonPkmnCatchType | None = None
        if pkmnCatchBoosterPack.catchType is not None:
            funtoonPkmnCatchType = self.__toFuntoonPkmnCatchType(pkmnCatchBoosterPack)

        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        actionCompleted = False

        if generalSettings.isFuntoonApiEnabled() and await self.__funtoonRepository.pkmnCatch(
            twitchChannel = twitchUser.getHandle(),
            twitchChannelId = await twitchChannel.getTwitchChannelId(),
            userThatRedeemed = twitchChannelPointsMessage.userName,
            funtoonPkmnCatchType = funtoonPkmnCatchType
        ):
            actionCompleted = True

        if not actionCompleted and generalSettings.isFuntoonTwitchChatFallbackEnabled():
            await self.__twitchUtils.safeSend(twitchChannel, f'!catch {twitchChannelPointsMessage.userName}')
            actionCompleted = True

        self.__timber.log('PkmnCatchRedemption', f'Redeemed pkmn catch for {twitchChannelPointsMessage.userName}:{twitchChannelPointsMessage.userId} (catch type: {pkmnCatchBoosterPack.catchType}) in {twitchUser.getHandle()}')
        return actionCompleted

    def __toFuntoonPkmnCatchType(
        self,
        pkmnCatchBoosterPack: PkmnCatchBoosterPack
    ) -> FuntoonPkmnCatchType:
        if not isinstance(pkmnCatchBoosterPack, PkmnCatchBoosterPack):
            raise TypeError(f'pkmnCatchBoosterPack argument is malformed: \"{pkmnCatchBoosterPack}\"')

        match pkmnCatchBoosterPack.catchType:
            case PkmnCatchType.GREAT: return FuntoonPkmnCatchType.GREAT
            case PkmnCatchType.NORMAL: return FuntoonPkmnCatchType.NORMAL
            case PkmnCatchType.ULTRA: return FuntoonPkmnCatchType.ULTRA
            case _: raise ValueError(f'unknown PkmnCatchType: \"{pkmnCatchBoosterPack.catchType}\"')
