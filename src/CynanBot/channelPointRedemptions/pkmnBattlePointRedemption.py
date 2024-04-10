import CynanBot.misc.utils as utils
from CynanBot.channelPointRedemptions.absChannelPointRedemption import \
    AbsChannelPointRedemption
from CynanBot.funtoon.funtoonRepositoryInterface import \
    FuntoonRepositoryInterface
from CynanBot.generalSettingsRepository import GeneralSettingsRepository
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.configuration.twitchChannel import TwitchChannel
from CynanBot.twitch.configuration.twitchChannelPointsMessage import \
    TwitchChannelPointsMessage
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface


class PkmnBattlePointRedemption(AbsChannelPointRedemption):

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

        if not twitchUser.isPkmnEnabled():
            return False

        splits = utils.getCleanedSplits(twitchChannelPointsMessage.getRedemptionMessage())

        if splits is None or len(splits) == 0:
            await self.__twitchUtils.safeSend(twitchChannel, f'⚠ Sorry @{twitchChannelPointsMessage.getUserName()}, you must specify the exact user name of the person you want to fight')
            return False

        opponentUserName = utils.removePreceedingAt(splits[0])
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        actionCompleted = False

        if generalSettings.isFuntoonApiEnabled() and await self.__funtoonRepository.pkmnBattle(
            twitchChannel = twitchUser.getHandle(),
            twitchChannelId = await twitchChannel.getTwitchChannelId(),
            userThatRedeemed = twitchChannelPointsMessage.getUserName(),
            userToBattle = opponentUserName
        ):
            actionCompleted = True

        if not actionCompleted and generalSettings.isFuntoonTwitchChatFallbackEnabled():
            await self.__twitchUtils.safeSend(twitchChannel, f'!battle {twitchChannelPointsMessage.getUserName()} {opponentUserName}')
            actionCompleted = True

        self.__timber.log('PkmnBattleRedemption', f'Redeemed pkmn battle for {twitchChannelPointsMessage.getUserName()}:{twitchChannelPointsMessage.getUserId()} in {twitchUser.getHandle()}')
        return actionCompleted

