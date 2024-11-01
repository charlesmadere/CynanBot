from .absChannelPointRedemption import AbsChannelPointRedemption
from ..funtoon.funtoonRepositoryInterface import FuntoonRepositoryInterface
from ..misc.generalSettingsRepository import GeneralSettingsRepository
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchChannel import TwitchChannel
from ..twitch.configuration.twitchChannelPointsMessage import TwitchChannelPointsMessage
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface


class PkmnEvolvePointRedemption(AbsChannelPointRedemption):

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

        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        actionCompleted = False

        if generalSettings.isFuntoonApiEnabled() and await self.__funtoonRepository.pkmnGiveEvolve(
            twitchChannel = twitchUser.getHandle(),
            twitchChannelId = await twitchChannel.getTwitchChannelId(),
            userThatRedeemed = twitchChannelPointsMessage.userName
        ):
            actionCompleted = True

        if not actionCompleted and generalSettings.isFuntoonTwitchChatFallbackEnabled():
            await self.__twitchUtils.safeSend(twitchChannel, f'!freeevolve {twitchChannelPointsMessage.userName}')
            actionCompleted = True

        self.__timber.log('PkmnEvolveRedemption', f'Redeemed pkmn evolve for {twitchChannelPointsMessage.userName}:{twitchChannelPointsMessage.userId} in {twitchUser.getHandle()}')
        return actionCompleted
