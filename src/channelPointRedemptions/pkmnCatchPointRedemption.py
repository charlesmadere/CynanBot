from typing import Final

from .absChannelPointRedemption import AbsChannelPointRedemption
from ..funtoon.funtoonHelperInterface import FuntoonHelperInterface
from ..funtoon.funtoonPkmnCatchType import FuntoonPkmnCatchType
from ..misc.generalSettingsRepository import GeneralSettingsRepository
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchChannel import TwitchChannel
from ..twitch.configuration.twitchChannelPointsMessage import TwitchChannelPointsMessage
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
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage,
    ) -> bool:
        twitchUser = twitchChannelPointsMessage.twitchUser
        if not twitchUser.isPkmnEnabled:
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

        if generalSettings.isFuntoonApiEnabled() and await self.__funtoonHelper.pkmnCatch(
            twitchChannel = twitchUser.handle,
            twitchChannelId = twitchChannelPointsMessage.twitchChannelId,
            userThatRedeemed = twitchChannelPointsMessage.userName,
            funtoonPkmnCatchType = funtoonPkmnCatchType,
        ):
            actionCompleted = True

        if not actionCompleted and generalSettings.isFuntoonTwitchChatFallbackEnabled():
            self.__twitchChatMessenger.send(
                text = f'!catch {twitchChannelPointsMessage.userName}',
                twitchChannelId = twitchChannelPointsMessage.twitchChannelId,
            )
            actionCompleted = True

        self.__timber.log('PkmnCatchRedemption', f'Redeemed for {twitchChannelPointsMessage.userName}:{twitchChannelPointsMessage.userId} in {twitchUser.handle} ({pkmnCatchBoosterPack=})')
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
