import traceback
from typing import Final

from .absChannelPointRedemption2 import AbsChannelPointRedemption2
from ..misc import utils as utils
from ..redemptionCounter.exceptions import RedemptionCounterNoSuchUserException, RedemptionCounterIsDisabledException
from ..redemptionCounter.helpers.redemptionCounterHelperInterface import RedemptionCounterHelperInterface
from ..redemptionCounter.settings.redemptionCounterSettingsInterface import RedemptionCounterSettingsInterface
from ..timber.timberInterface import TimberInterface
from ..trollmoji.trollmojiHelperInterface import TrollmojiHelperInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChannelPointsRedemption import TwitchChannelPointsRedemption


class RedemptionCounterPointRedemption(AbsChannelPointRedemption2):

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

    async def handlePointRedemption(
        self,
        channelPointsRedemption: TwitchChannelPointsRedemption,
    ) -> bool:
        twitchUser = channelPointsRedemption.twitchUser
        if not twitchUser.areRedemptionCountersEnabled:
            return False

        boosterPacks = twitchUser.redemptionCounterBoosterPacks
        if boosterPacks is None or len(boosterPacks) == 0:
            return False

        boosterPack = boosterPacks.get(channelPointsRedemption.rewardId, None)
        if boosterPack is None:
            return False

        try:
            result = await self.__redemptionCounterHelper.increment(
                incrementAmount = boosterPack.incrementAmount,
                chatterUserId = channelPointsRedemption.redemptionUserId,
                counterName = boosterPack.counterName,
                twitchChannelId = channelPointsRedemption.twitchChannelId,
            )
        except RedemptionCounterIsDisabledException as e:
            self.__timber.log('RedemptionCounterPointRedemption', f'Redemption Counter feature is currently disabled ({channelPointsRedemption=}) ({boosterPack=})', e, traceback.format_exc())
            return True
        except RedemptionCounterNoSuchUserException as e:
            self.__timber.log('RedemptionCounterPointRedemption', f'Unable to find the user of the given user ID ({channelPointsRedemption=}) ({boosterPack=})', e, traceback.format_exc())
            return True

        prefixEmote = await self.__trollmojiHelper.getDinkDonkEmote()
        if not utils.isValidStr(prefixEmote):
            prefixEmote = 'ⓘ'

        suffixEmote = ''
        if utils.isValidStr(boosterPack.emote):
            suffixEmote = boosterPack.emote

        self.__twitchChatMessenger.send(
            text = f'{prefixEmote} @{channelPointsRedemption.redemptionUserName} has a new {result.counterName} count of {result.countStr}! {suffixEmote}',
            twitchChannelId = channelPointsRedemption.twitchChannelId,
        )

        self.__timber.log('RedemptionCounterPointRedemption', f'Redeemed ({channelPointsRedemption=}) ({boosterPack=}) ({result=})')
        return True
