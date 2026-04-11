import traceback
from typing import Final

from .absChannelPointsRedemption import AbsChannelPointRedemption
from .pointsRedemptionResult import PointsRedemptionResult
from ..misc import utils as utils
from ..redemptionCounter.exceptions import RedemptionCounterNoSuchUserException, RedemptionCounterIsDisabledException
from ..redemptionCounter.helpers.redemptionCounterHelperInterface import RedemptionCounterHelperInterface
from ..redemptionCounter.settings.redemptionCounterSettingsInterface import RedemptionCounterSettingsInterface
from ..timber.timberInterface import TimberInterface
from ..trollmoji.trollmojiHelperInterface import TrollmojiHelperInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChannelPointsRedemption import TwitchChannelPointsRedemption
from ..users.userInterface import UserInterface


class RedemptionCounterPointRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        redemptionCounterHelper: RedemptionCounterHelperInterface,
        redemptionCounterSettings: RedemptionCounterSettingsInterface,
        timber: TimberInterface,
        trollmojiHelper: TrollmojiHelperInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(redemptionCounterHelper, RedemptionCounterHelperInterface):
            raise TypeError(f'redemptionCounterHelper argument is malformed: \"{redemptionCounterHelper}\"')
        elif not isinstance(redemptionCounterSettings, RedemptionCounterSettingsInterface):
            raise TypeError(f'redemptionCounterSettings argument is malformed: \"{redemptionCounterSettings}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(trollmojiHelper, TrollmojiHelperInterface):
            raise TypeError(f'trollmojiHelper argument is malformed: \"{trollmojiHelper}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__redemptionCounterHelper: Final[RedemptionCounterHelperInterface] = redemptionCounterHelper
        self.__redemptionCounterSettings: Final[RedemptionCounterSettingsInterface] = redemptionCounterSettings
        self.__timber: Final[TimberInterface] = timber
        self.__trollmojiHelper: Final[TrollmojiHelperInterface] = trollmojiHelper
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

    async def handlePointsRedemption(
        self,
        pointsRedemption: TwitchChannelPointsRedemption,
    ) -> PointsRedemptionResult:
        twitchUser = pointsRedemption.twitchUser
        if not twitchUser.areRedemptionCountersEnabled:
            return PointsRedemptionResult.IGNORED

        boosterPacks = twitchUser.redemptionCounterBoosterPacks
        if boosterPacks is None or len(boosterPacks) == 0:
            return PointsRedemptionResult.IGNORED

        boosterPack = boosterPacks.get(pointsRedemption.rewardId, None)
        if boosterPack is None:
            return PointsRedemptionResult.IGNORED

        try:
            result = await self.__redemptionCounterHelper.increment(
                incrementAmount = boosterPack.incrementAmount,
                chatterUserId = pointsRedemption.redemptionUserId,
                counterName = boosterPack.counterName,
                twitchChannelId = pointsRedemption.twitchChannelId,
            )
        except RedemptionCounterIsDisabledException as e:
            self.__timber.log(self.pointsRedemptionName, f'Redemption Counter feature is currently disabled ({boosterPack=}) ({pointsRedemption=})', e, traceback.format_exc())
            return PointsRedemptionResult.CONSUMED
        except RedemptionCounterNoSuchUserException as e:
            self.__timber.log(self.pointsRedemptionName, f'Unable to find the user of the given user ID ({boosterPack=}) ({pointsRedemption=})', e, traceback.format_exc())
            return PointsRedemptionResult.CONSUMED

        prefixEmote = await self.__trollmojiHelper.getDinkDonkEmote()
        if not utils.isValidStr(prefixEmote):
            prefixEmote = 'ⓘ'

        suffixEmote = ''
        if utils.isValidStr(boosterPack.emote):
            suffixEmote = boosterPack.emote

        self.__twitchChatMessenger.send(
            text = f'{prefixEmote} @{pointsRedemption.redemptionUserName} has a new {result.counterName} count of {result.countStr}! {suffixEmote}',
            twitchChannelId = pointsRedemption.twitchChannelId,
        )

        self.__timber.log(self.pointsRedemptionName, f'Redeemed ({result=}) ({boosterPack=}) ({pointsRedemption=})')
        return PointsRedemptionResult.CONSUMED

    @property
    def pointsRedemptionName(self) -> str:
        return 'RedemptionCounterPointRedemption'

    def relevantRewardIds(
        self,
        twitchUser: UserInterface,
    ) -> frozenset[str]:
        boosterPacks = twitchUser.redemptionCounterBoosterPacks
        rewardIds: set[str] = set()

        if boosterPacks is not None and len(boosterPacks.keys()) >= 1:
            rewardIds.update(boosterPacks.keys())

        return frozenset(rewardIds)
