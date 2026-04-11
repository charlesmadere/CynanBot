from typing import Final

from .absChannelPointsRedemption2 import AbsChannelPointRedemption2
from .pointsRedemptionResult import PointsRedemptionResult
from ..funtoon.funtoonHelperInterface import FuntoonHelperInterface
from ..misc import utils as utils
from ..misc.generalSettingsRepository import GeneralSettingsRepository
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChannelPointsRedemption import TwitchChannelPointsRedemption
from ..users.userInterface import UserInterface


class PkmnBattlePointRedemption(AbsChannelPointRedemption2):

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

    async def handlePointsRedemption(
        self,
        pointsRedemption: TwitchChannelPointsRedemption,
    ) -> PointsRedemptionResult:
        if not pointsRedemption.twitchUser.isPkmnEnabled:
            return PointsRedemptionResult.IGNORED

        splits = utils.getCleanedSplits(pointsRedemption.redemptionMessage)
        if splits is None or len(splits) == 0 or not utils.isValidStr(splits[0]):
            self.__twitchChatMessenger.send(
                text = f'⚠ Sorry @{pointsRedemption.redemptionUserName}, you must specify the exact user name of the person you want to fight',
                twitchChannelId = pointsRedemption.twitchChannelId,
            )
            return PointsRedemptionResult.CONSUMED

        opponentUserName = utils.removePreceedingAt(splits[0])
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        actionCompleted = False

        if generalSettings.isFuntoonApiEnabled() and await self.__funtoonHelper.pkmnBattle(
            twitchChannel = pointsRedemption.twitchChannel,
            twitchChannelId = pointsRedemption.twitchChannelId,
            userThatRedeemed = pointsRedemption.redemptionUserName,
            userToBattle = opponentUserName,
        ):
            actionCompleted = True

        if not actionCompleted and generalSettings.isFuntoonTwitchChatFallbackEnabled():
            self.__twitchChatMessenger.send(
                text = f'!battle {pointsRedemption.redemptionUserName} {opponentUserName}',
                twitchChannelId = pointsRedemption.twitchChannelId,
            )
            actionCompleted = True

        self.__timber.log(self.pointsRedemptionName, f'Redeemed ({actionCompleted=}) ({pointsRedemption=})')
        return PointsRedemptionResult.CONSUMED

    @property
    def pointsRedemptionName(self) -> str:
        return 'PkmnBattlePointRedemption'

    def relevantRewardIds(
        self,
        twitchUser: UserInterface,
    ) -> frozenset[str]:
        rewardId = twitchUser.pkmnBattleRewardId

        if utils.isValidStr(rewardId):
            return frozenset({ rewardId })
        else:
            return frozenset()
