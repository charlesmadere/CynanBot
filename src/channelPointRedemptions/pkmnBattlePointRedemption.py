from typing import Final

from .absChannelPointRedemption import AbsChannelPointRedemption
from ..funtoon.funtoonHelperInterface import FuntoonHelperInterface
from ..misc import utils as utils
from ..misc.generalSettingsRepository import GeneralSettingsRepository
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChannelPointsRedemption import TwitchChannelPointsRedemption


class PkmnBattlePointRedemption(AbsChannelPointRedemption):

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

        splits = utils.getCleanedSplits(channelPointsRedemption.redemptionMessage)

        if splits is None or len(splits) == 0:
            self.__twitchChatMessenger.send(
                text = f'⚠ Sorry @{channelPointsRedemption.redemptionUserName}, you must specify the exact user name of the person you want to fight',
                twitchChannelId = channelPointsRedemption.twitchChannelId,
            )
            return False

        opponentUserName = utils.removePreceedingAt(splits[0])
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        actionCompleted = False

        if generalSettings.isFuntoonApiEnabled() and await self.__funtoonHelper.pkmnBattle(
            twitchChannel = channelPointsRedemption.twitchChannel,
            twitchChannelId = channelPointsRedemption.twitchChannelId,
            userThatRedeemed = channelPointsRedemption.redemptionUserName,
            userToBattle = opponentUserName,
        ):
            actionCompleted = True

        if not actionCompleted and generalSettings.isFuntoonTwitchChatFallbackEnabled():
            self.__twitchChatMessenger.send(
                text = f'!battle {channelPointsRedemption.redemptionUserName} {opponentUserName}',
                twitchChannelId = channelPointsRedemption.twitchChannelId,
            )
            actionCompleted = True

        self.__timber.log('PkmnBattleRedemption', f'Redeemed ({channelPointsRedemption=}) ({actionCompleted=})')
        return actionCompleted
