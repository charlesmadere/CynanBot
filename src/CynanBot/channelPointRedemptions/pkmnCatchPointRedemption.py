from CynanBot.channelPointRedemptions.absChannelPointRedemption import \
    AbsChannelPointRedemption
from CynanBot.funtoon.funtoonPkmnCatchType import FuntoonPkmnCatchType
from CynanBot.funtoon.funtoonRepositoryInterface import \
    FuntoonRepositoryInterface
from CynanBot.generalSettingsRepository import GeneralSettingsRepository
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.configuration.twitchChannel import TwitchChannel
from CynanBot.twitch.configuration.twitchChannelPointsMessage import \
    TwitchChannelPointsMessage
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.users.pkmnCatchBoosterPack import PkmnCatchBoosterPack
from CynanBot.users.pkmnCatchType import PkmnCatchType
from CynanBot.users.user import User


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
        twitchUser = twitchChannelPointsMessage.getTwitchUser()

        if not isinstance(twitchUser, User):
            # dumb hack, idk what to do about this for now. regardless this should never ever
            # happen under the current codebase
            self.__timber.log('PkmnCatchRedemption', f'Received a UserInterface instance that was not a User instance: \"{twitchUser}\"')
            return False
        elif not twitchUser.isPkmnEnabled() or not twitchUser.hasPkmnCatchBoosterPacks():
            return False

        pkmnCatchBoosterPacks = twitchUser.getPkmnCatchBoosterPacks()

        if pkmnCatchBoosterPacks is None or len(pkmnCatchBoosterPacks) == 0:
            return False

        pkmnCatchBoosterPack: PkmnCatchBoosterPack | None = None

        for pkbp in pkmnCatchBoosterPacks:
            if twitchChannelPointsMessage.getRewardId() == pkbp.rewardId:
                pkmnCatchBoosterPack = pkbp
                break

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
            userThatRedeemed = twitchChannelPointsMessage.getUserName(),
            funtoonPkmnCatchType = funtoonPkmnCatchType
        ):
            actionCompleted = True

        if not actionCompleted and generalSettings.isFuntoonTwitchChatFallbackEnabled():
            await self.__twitchUtils.safeSend(twitchChannel, f'!catch {twitchChannelPointsMessage.getUserName()}')
            actionCompleted = True

        self.__timber.log('PkmnCatchRedemption', f'Redeemed pkmn catch for {twitchChannelPointsMessage.getUserName()}:{twitchChannelPointsMessage.getUserId()} (catch type: {pkmnCatchBoosterPack.catchType}) in {twitchUser.getHandle()}')
        return actionCompleted

    def __toFuntoonPkmnCatchType(
        self,
        pkmnCatchBoosterPack: PkmnCatchBoosterPack
    ) -> FuntoonPkmnCatchType:
        if not isinstance(pkmnCatchBoosterPack, PkmnCatchBoosterPack):
            raise TypeError(f'pkmnCatchBoosterPack argument is malformed: \"{pkmnCatchBoosterPack}\"')

        if pkmnCatchBoosterPack.catchType is PkmnCatchType.NORMAL:
            return FuntoonPkmnCatchType.NORMAL
        elif pkmnCatchBoosterPack.catchType is PkmnCatchType.GREAT:
            return FuntoonPkmnCatchType.GREAT
        elif pkmnCatchBoosterPack.catchType is PkmnCatchType.ULTRA:
            return FuntoonPkmnCatchType.ULTRA
        else:
            raise ValueError(f'unknown PkmnCatchType: \"{pkmnCatchBoosterPack.catchType}\"')
